#!/usr/bin/python
from __future__ import absolute_import
import json
import os
import sys
import shlex
import subprocess
from collections import OrderedDict

import docker
from toil.common import Toil
from toil.job import Job

from . import bam_load_check
from . import bed_check_sort_reg
from . import gvc_check
from . import gvc_pipeline
from . import qc_pipeline
from . import predict
from . import vcf_oncodecode
from . import license_job
from . import cnv
import pysam
import copy
import itertools
import argparse
# import variant_interface

import re


def remap_bam(ref, bam, thread, docker, volumes):
    # https://www.biostars.org/p/134638/
    # samtools fastq reads.bam | bwa mem -p ref.fa -
    oldbam = bam + '.old.bam'
    os.rename(bam, oldbam)
    os.rename(bam + '.bai', oldbam + '.bai')
    vol_str = ''
    for k in volumes.keys():
        vol_str = vol_str + ' -v ' + k + ':' + k + ' '
    # docker run -v /db:/db -v/disk:/disk bwa_bam_pipe:1.0-8-g09a12df sh -c \
    # "samtools fastq /disk/bam2vcf/data/T.bam.old.bam | bwa mem -t 12 -p \
    # /db/WEBtool/ref/human.fa -
    # | samtools view -@ 12  -b -T /db/WEBtool/ref/human.fa -S - \
    # | samtools sort -@ 12 - -o /disk/bam2vcf/data/T.bam
    # && samtools index /disk/bam2vcf/data/T.bam"
    cmd = ('docker run ' + vol_str + docker + ' sh -c "samtools fastq ' +
           oldbam + ' | bwa mem -t ' + thread + ' -p ' + ref + ' - ' +
           ' | samtools view -@ ' + thread + ' -b -T ' + ref + ' -S - ' +
           ' | samtools sort -@ ' + thread + ' - -o ' + bam +
           ' && samtools index ' + bam + '"')
    print(cmd)
    subprocess.call(shlex.split(cmd))
    return True


def cmd_parser(absPath):
    parser = Job.Runner.getDefaultArgumentParser()
    parser.add_argument(
        'input_json',
        help='The json file stores names and paths of both normal and tumor samples.'
        + '\n' +
        'eg: {"N": ["/disk/N.sort.dup.bam"], "T": ["/disk/T.sort.dup.bam"]}')
    parser.add_argument('reference', help='The reference fasta file')
    parser.add_argument('outpath', help='The output folder')
    parser.add_argument(
        '--dbsnp',
        help="The Single Nucleotide Polymorphism Database(dbSNP) file", required=True)
    parser.add_argument(
        '--bed',
        help="""BED file for WES or Panel analysis. It should be a TAB delimited file
with at least three columns: chrName, startPosition and endPostion""")
    parser.add_argument(
        '--segmentSize',
        help="Chromosome segment size for each GVC job, set to 100000000 (100MB) or larger for better performance. Default is to run only one GVC job.")
    parser.add_argument(
        '--gvc_lib',
        help="GVC library folder",
        required=True)

    parser.add_argument(
        '--region',
        help=argparse.SUPPRESS
    )
    parser.add_argument('--strategy', choices=['WES', 'WGS', 'Panel'],
                        help='Switch algorithm for WES, Panel or WGS analysis')
    parser.add_argument(
        '--mutantType',
        help="Switch algorithm for germline or somatic mutation detection",
        choices=['Somatic', 'Germline'],
        action='append',
        default=[])
    parser.add_argument('--CNV', action='store_true', default=False,
                        help='calculate and output CNV simultaneously')
    parser.add_argument('--SV', action='store_true', default=False,
                        help='calculate and output SV simultaneously')
    parser.add_argument(
        '--sample_name', help="Name of the sample to be analyzed.", default='sample_name')
    parser.add_argument('--rmtmp', action='store_true',
                        default=False, help='remove tempelate file')

    return parser.parse_args()


def check_dir_volume(name, paramter, file_path, msg=None):
    if not file_path:
        print("ERROR:{0} is None,please check paramter{1}.".format(
            name, paramter))
        sys.exit(-1)

    if not isinstance(file_path, str) and not isinstance(file_path, unicode):
        print (type(file_path))
        print("filepath is not string")
        sys.exit(-2)
    if os.path.exists(file_path) is False:
        print("ERROR:{0} file not found:{1}".format(name, file_path))
        if msg:
            print(msg)
        sys.exit(-3)


def check_images_exist(version):
    client = docker.from_env()
    for val in version.values():
        try:
            client.images.get(val)
        except docker.errors.ImageNotFound as E:
            print(val, "images can't found")
            sys.exit(4)
        except Exception as E:
            print(E)
            sys.exit(5)


def get_link_files(v_path):
    #print ("get_link_files:",v_path,os.path.realpath(v_path))
    if os.path.isfile(v_path) and os.path.realpath(v_path) != v_path:
        return [os.path.realpath(v_path)]
    elif os.path.realpath(v_path) != v_path:
        return []

    vpath_inner = [map(lambda x: os.path.join(root, x), files)
                   for root, _, files in os.walk(v_path)]
    return filter(lambda x: x != os.path.realpath(x), list(itertools.chain.from_iterable(vpath_inner)))


def get_dynamic_volumes(*intput_paths):
    paths = map(lambda x: os.path.abspath(re.sub('/+', '/', x)), intput_paths)
    links = map(get_link_files, paths)
    subpath = list(itertools.chain.from_iterable(links))
    subpath.extend(paths)
    dirpaths = map(lambda x: os.path.dirname(
        x) if os.path.isfile(x) else x, subpath)
    realpahts = map(os.path.realpath, dirpaths)
    dirpaths.extend(realpahts)
    dirpaths = map(lambda x: '/'.join(x.split('/')[:2]), dirpaths)
    bindpaths = map(lambda x: {'bind': x, 'mode': 'rw'}, dirpaths)
    return dict(zip(dirpaths, bindpaths))


def bam_vcf_pipeline(root, gvc_lib, reference, dbsnp, strategy, bed, outpath, group_info, mutantType, segmentSize,
                     sample_name, model_path, check_bam, enable_vcf_oncodecode=False, CNV_enable=True, SV_enable=True, rm_temp=True, volumes=None, limit_regions=None):
    variants = ['snv', 'indel', 'sv']
    gvc_varians = ['snv', 'indel', 'cnv', 'sv']
    filtermodel = ['grig', 'xgboost', 'filter']
    if not CNV_enable:
        gvc_varians.remove('cnv')

    if not SV_enable:
        variants.remove('sv')
        gvc_varians.remove('sv')

    # check version volumes file path
    version_path = gvc_lib + '/version.json'
    #volumes_path = gvc_lib + '/volumes.json'
    #thread_path = gvc_lib + '/thread.json'
    xml_path = gvc_lib + '/format.xml'

    #check_dir_volume("volumn", "--gvc_lib", volumes_path)
    check_dir_volume("version", "--gvc_lib", version_path)
    #check_dir_volume("thread", "--gvc_lib", thread_path)
    check_dir_volume("xml", "--gvc_lib", xml_path)
    check_dir_volume("Module", "--gvc_lib", model_path)

    with open(version_path, 'r') as verf:
        version = json.load(verf)

    # with open(thread_path, 'r') as thref:
    #     thread = json.load(thref)

    # check fa and fa.fai
    check_dir_volume("Reference ", "reference", reference)
    check_dir_volume("fai", "reference", reference + '.fai',
                     "please user samtools: samtools faidx {}".format(reference))

    # check docker images
    # check_images_exist(version)
    # check dbsnp dir
    check_dir_volume("dbsnp frequency", "--dbsnp", dbsnp)

    # check output dir and volumes dir
    check_dir_volume("outpath", "outpath", outpath)
    # check bed dir
    if strategy == 'WES' or strategy == 'Panel':
        check_dir_volume("bed", "--bed", bed)
        bed_sort_file = outpath + '/' + os.path.basename(bed) + '.sort'
        bed_check_sort_reg.bed_check_sort_reg(reference, bed, bed_sort_file)
    # tmp dir
    temp = outpath + '/tmp/'
    if os.path.exists(temp) is False:
        os.makedirs(temp)
    # Bam list
    for skey in group_info.keys():
        if len(group_info[skey]) > 1:
            print("ERROR: At current version, we only support one bam file " +
                  "for tumor sample and one bam file for normal sample.")
            sys.exit(1)
    if len(group_info) == 1 or len(group_info['N'][0]) == 0:
        if len(group_info['T'][0]) > 1:
            bam_list = group_info['T']
            group_info = {'T': group_info['T']}
            if 'Somatic' in mutantType:
                print(
                    "ERROR: At current version, we only support Germline for Single-sample.")
                sys.exit(1)
            mutantType = ['Germline']
        else:
            print("ERROR: The json file format is error. the format is " +
                  '{"T": ["/disk/T.sort.dup.bam"]}')
            sys.exit(1)

    if mutantType != ['Germline']:
        bam_list = group_info['N'] + group_info['T']
        group_info = OrderedDict(zip(['N', 'T'], bam_list))
    else:
        bam_list = group_info['T']
        group_info = {'T': group_info['T']}

    bam_list = map(os.path.abspath, bam_list)

    if not volumes:
        if bed:
            volumes = get_dynamic_volumes(
                reference, model_path, gvc_lib, dbsnp, bed, outpath, *bam_list)
        else:
            volumes = get_dynamic_volumes(
                reference, model_path, gvc_lib, dbsnp, outpath, *bam_list)
        # print(gvc_lib)
        #print ("*******volumes:",volumes)
        # sys.exit(-1)
    if check_bam:
        if mutantType == ['Germline']:
            check_dir_volume("bam", "input_json", group_info['T'][0])
        else:
            check_dir_volume("bam", "input_json", group_info['N'][0])
            check_dir_volume("bam", "input_json", group_info['T'][0])

        for bam in bam_list:
            bam_load_check.bamBai(bam)
            bam_ref_logical = bam_load_check.bamRefCheck(reference,
                                                         bam)
            if bam_ref_logical is False:
                print ('Chromosome name in bam file is different from reference.\
                     Check {} for correct chromosome names.'.format(bam))
                sys.exit(-1)

    if strategy == 'WGS':
        bed_sort_file = None

    gvc_volumes = copy.deepcopy(volumes)
    gvc_volumes[gvc_lib] = {
        "bind": "/Genowis",
        "mode": "rw"
    }
    check_license_job = license_job.verify_license(
        version['xgboost'], gvc_volumes)
    root.addChild(check_license_job)
    root = root.encapsulate()
    feature_dict = gvc_pipeline.gvc_pipeline(
        root,
        reference,
        segmentSize,
        bam_list,
        temp,
        sample_name,
        version,
        gvc_volumes,
        gvc_varians,
        rm_gvcs=True,
        dbsnp=dbsnp,
        ccd=bed_sort_file,
        limit_regions=limit_regions)
    root = root.encapsulate()
    #print (group_info.keys(),bam_list)

    if CNV_enable and 'Somatic' in mutantType:
        new_volumes = copy.deepcopy(volumes)
        new_volumes[os.path.join(gvc_lib, 'database', 'CNV')] = {
            "bind": "/disk/software/GVC-CNV/",
            "mode": "rw"
        }
        cnv_job = cnv.cnv(sample_name, os.path.basename(
            feature_dict['cnv'][0]), os.path.basename(feature_dict['cnv'][1]), outpath, group_info.keys(), os.path.dirname(feature_dict['cnv'][0]), version['cnv'], new_volumes, enable_panel=strategy == 'Panel')
        root.addChild(cnv_job)

    if strategy == 'Panel':
        strategy = "Panel_tissue"
    seqtype = "Hiseq"
    if strategy == 'WGS':
        if os.path.exists(reference + '.reg') is False:
            qc_pipeline.rootUpdateJob_pipeline(
                root, reference, None, strategy, version, volumes)
            root = root.encapsulate()

    qc_txts = qc_pipeline.qc_pipeline(root, temp, outpath, strategy, bam_list, group_info.keys(
    ), reference, bed_sort_file, sample_name, version, volumes)

    root = root.encapsulate()
    setting_dict = qc_pipeline.qc2predict(
        root, qc_txts, temp, group_info.keys(), seqtype, strategy,
        variants, mutantType, version, volumes)

    predict_volumes = copy.deepcopy(volumes)
    predict_volumes[gvc_lib] = {
        "bind": "/Genowis",
        "mode": "rw"
    }

    root = root.encapsulate()
    # predict
    if strategy == 'WGS':
        predict_dict = predict.Predict_pipeline(root, sample_name,
                                                group_info.keys(), outpath,
                                                setting_dict, feature_dict, variants, seqtype,
                                                strategy, mutantType, None,
                                                filtermodel, xml_path, model_path, bam_list[-1], version,
                                                predict_volumes)
    elif strategy == 'WES' or strategy == "Panel_tissue":
        predict_dict = predict.Predict_pipeline(root, sample_name,
                                                group_info.keys(), outpath,
                                                setting_dict, feature_dict, variants, seqtype,
                                                strategy, mutantType, bed_sort_file,
                                                filtermodel, xml_path, model_path, bam_list[-1], version,
                                                predict_volumes)
    root = root.encapsulate()
    if 'Somatic' in mutantType:
        predict.post_filter(root, predict_dict, [
                            'snv', 'indel'], reference, bam_list[-1], sample_name, outpath, version, volumes)
        root = root.encapsulate()
    # vcf_oncodecode
    if enable_vcf_oncodecode:
        vcf_oncodecode.run_vcf_oncodecode(
            root, outpath, sample_name, variants, filtermodel,
            mutantType, strategy, version, volumes)
        root = root.encapsulate()
    # rm predict tmp

    if rm_temp:
        if strategy in ('WES', "Panel_tissue"):
            predict.tmp_rm_def(
                root,
                sample_name,
                outpath,
                variants,
                filtermodel,
                strategy,
                mutantType,
                rm_predict=True, bed=bed)
        else:
            predict.tmp_rm_def(
                root,
                sample_name,
                outpath,
                variants,
                filtermodel,
                strategy,
                mutantType,
                rm_predict=True, bed=None)
    return root


def get_bam_lengths(group_info):
    choice_length = [100, 150]
    limit = 10
    l_arv_reads_all_bams = list()
    for bams in group_info.values():
        for bam in bams:
            l_reads_bam = list()
            primary_reads = pysam.AlignmentFile(bam)
            for reads in primary_reads.fetch():
                if len(l_reads_bam) > 10:
                    break
                if (reads.flag & (pysam.FSECONDARY | pysam.FSUPPLEMENTARY)) > 0 and reads.flag & pysam.FUNMAP == 0:
                    l_reads_bam.append(reads.infer_read_length())

            l_arv_reads_all_bams.append(sum(l_reads_bam)/len(l_reads_bam))
            primary_reads.close()
    arv_len = sum(l_arv_reads_all_bams) / len(l_arv_reads_all_bams)
    return min(choice_length, key=lambda x: abs(x-arv_len))


def get_model_path(gvc_lib_path, choice_length):
    return '{}/Model/PE{}'.format(gvc_lib_path, choice_length)


if __name__ == "__main__":

    absPath = os.path.abspath(os.path.dirname(sys.argv[0]))
    options = cmd_parser(absPath)
    options.stats = True

    license_volum = {
        options.gvc_lib: {"bind": "/Genowis",
                                  "mode": "rw"}
    }
    start_job = Job()
    # load bam
    check_dir_volume('input_json', 'input_json', options.input_json)

    limit_regions = gvc_pipeline.get_regions_file(options.region)
    with open(options.input_json) as fp:
        group_info = json.load(fp, object_pairs_hook=OrderedDict)

    model_length = get_bam_lengths(group_info)
    model_path = get_model_path(options.gvc_lib, model_length)
    start_job = bam_vcf_pipeline(start_job, options.gvc_lib, options.reference, options.dbsnp, options.strategy, options.bed,
                                 options.outpath, group_info, options.mutantType, options.segmentSize,
                                 options.sample_name, model_path, check_bam=True, CNV_enable=options.CNV, SV_enable=options.SV, rm_temp=options.rmtmp,limit_regions=limit_regions)
    #vd = variant_interface.VariantFeature()
    #print (vd.get_feature('snv'))
    with Toil(options) as toil:
        if not toil.options.restart:
            toil.start(start_job)
        else:
            toil.restart()
