from toil.common import Toil
from toil.job import Job

import pwd
import getpass
import argparse
import subprocess
import commands
import pysam
import os
import sys
import json
import docker
import time
import re
import variant_interface
from runner.runner import docker_runner, decorator_wrapt


class GVC(Job):
    @decorator_wrapt
    def __init__(self, input_bam, intput_ref, output_path,  image, volumes, variants, reg=None, freg=None, dbsnp=None, ccd=None, bed=None, *args, **kwargs):
        self.image = image
        self.volumes = volumes
        self.commandLine = ['gvc', '-f', intput_ref]
        if isinstance(input_bam, list):
            for bam in input_bam:
                self.commandLine.extend(['--in', bam])
        else:
            self.commandLine.extend(['--in', self.input_bam])
        if reg and freg:
            self.commandLine.extend(
                ['--out', output_path + '.' + freg, '--region', reg, '--fregion', freg])
        else:
            self.commandLine.extend(
                ['--out', output_path])
        if dbsnp:
            self.commandLine.extend(['--dbsnp', dbsnp])
        if ccd:
            self.commandLine.extend(['--ccd', ccd])
        if bed:
            self.commandLine.extend(['--bed', bed])
        for variant in variants:
            if variant == 'snv':
                self.commandLine.extend(['--snp'])
            elif variant == 'indel':
                self.commandLine.extend(['--indel'])
            elif variant == 'cnv':
                self.commandLine.extend(['--ghs', '--cov'])
            else:
                self.commandLine.extend(['--sv'])
        super(GVC, self).__init__(*args, **kwargs)

    @docker_runner('GVC')
    def run(self, fileStore):
        return self.commandLine


class catJob(Job):

    def __init__(self, intputList, outputName, rm_gvcs=False, *args, **kwargs):
        self.intputList = intputList
        self.rm_gvcs = rm_gvcs
        self.commandLine = ['cat']
        self.commandLine.extend(self.intputList)
        self.commandLine.extend(['>', outputName])
        self.outputfile = outputName
        super(catJob, self).__init__(*args, **kwargs)

    def run(self, fileStore):
        commands.getstatusoutput('\t'.join(self.commandLine))
        if self.rm_gvcs:
            for path in self.intputList:
                os.remove(path)

    def get_all_variant(self):
        return self.outputfile


def read_ccd(ccd_name):
    with open(ccd_name) as F:
        return map(lambda x: x.strip('\n').strip('\r').split('\t')[:3], F)


def filter_bed(ccd_regions, limit_size):
    return filter(lambda x: len(x[0]) < limit_size, ccd_regions)


def filter_references(references, reference_lengths, limit_size):
    l_filter_references = list()
    l_filter_reference_lengths = list()
    for i_ref, i_length in zip(references, reference_lengths):
        if len(i_ref) < limit_size:
            l_filter_references.append(i_ref)
            l_filter_reference_lengths.append(i_length)
    return l_filter_references, l_filter_reference_lengths


def split_reference(references, reference_lengths, segmentSize):
    list_intervals = list()
    for reference, reference_length in zip(references, reference_lengths):
        list_intervals.extend(map(lambda x: [
                              reference, x, x+segmentSize-1], range(1, reference_length, segmentSize)))
        if list_intervals[-1][2] > reference_length:
            list_intervals[-1][2] = reference_length
    return list_intervals


def split_ccd(ccd_region, segmentSize):
    regions = [[ccd_region[0][0], int(
        ccd_region[0][1]), int(ccd_region[0][2])]]
    for chrom, start, end in ccd_region[1:]:
        if chrom != regions[-1][0] or regions[-1][1] + segmentSize < int(end):
            regions.append([chrom, int(start), int(end)])
        else:
            regions[-1][2] = int(end)
    return regions


def get_regions(ccd_name, references, lengths, segmentSize, limit_regions=None):
    segmentSize = int(segmentSize)
    origin_regions = list()
    if ccd_name:
        origin_region = read_ccd(ccd_name)
        origin_regions = split_ccd(origin_region, segmentSize)
    else:
        origin_regions = split_reference(references, lengths, segmentSize)
    return filter(lambda x: limit_regions is None or x[0] in limit_regions, origin_regions)


def get_regions_file(reginos_file):
    if reginos_file is None:
        return None
    with open(reginos_file) as F:
        try:
            return map(lambda x: re.search('\s?(\S+)\S?', x).group(1), F)
        except Exception as E:
            print ("Regions Format Error")
            sys.exit(-1)


def gvc_pipeline(root, reference_filename, segmentSize, bam, outpath, sampleName, version, volumes, variants, rm_bam=False, rm_gvcs=True, dbsnp=None, ccd=None, limit_regions=None):
    Fasta = pysam.Fastafile(reference_filename)
    references = Fasta.references
    if segmentSize:
        region = get_regions(ccd, Fasta.references,
                             Fasta.lengths, segmentSize, limit_regions)
        if ccd:
            gvc_jobs = map(lambda x: GVC(bam, reference_filename,
                                         outpath + '/' + sampleName, version['gvc'], volumes, variants, str(
                                             x[0]) + ":" + str(x[1]) + "-" + str(x[2]),
                                         str(x[0]) + ":" + str(x[1]) + "-" + str(x[2]), dbsnp=dbsnp, ccd=ccd, bed=ccd, memory="8G"), region)
        else:
            gvc_jobs = map(lambda x: GVC(bam, reference_filename,
                                         outpath + '/' +
                                         sampleName, version['gvc'], volumes, variants,
                                         str(x[0]) + ":" + str(x[1]) +
                                         "-" + str(x[2] + 2500),
                                         str(x[0]) + ":" + str(x[1]) +
                                         "-" + str(x[2]),
                                         dbsnp=dbsnp, ccd=ccd, bed=ccd, memory="8G"), region)
        map(lambda job: root.addChild(job), gvc_jobs)
    else:
        gvc_jobs = GVC(bam, reference_filename, outpath + '/' + sampleName,
                       version['gvc'], volumes, variants, dbsnp=dbsnp, ccd=ccd, bed=ccd, memory="8G")
        root.addChild(gvc_jobs)
    if segmentSize:
        datatype = []
        for variant in variants:
            if variant == 'snv':
                datatype = datatype+['pup']
            elif variant == 'indel':
                datatype = datatype + ['idf']
            elif variant == 'sv':
                datatype = datatype + ['svf']
            elif variant == 'cnv':
                datatype = datatype + ['ghs', 'cov']
        cat_jobs = map(lambda suffix: catJob(
            map(lambda x: outpath + '.'.join([sampleName, str(x[0]) + ":" + str(x[1]) + "-" + str(x[2]), suffix]),
                region), outpath + '/' + '.'.join([sampleName, suffix]), rm_gvcs), datatype)
        map(lambda catPupJob: root.addFollowOn(catPupJob), cat_jobs)
    Fasta.close()
    vi = variant_interface.VariantFeature()
    vi.set_feature(
        "snv", outpath + '.'.join([sampleName, 'pup']))
    vi.set_feature(
        "indel", outpath + '.'.join([sampleName, 'idf']))
    vi.set_feature(
        "sv", outpath + '.'.join([sampleName, 'svf']))
    return {"snv": outpath + '.'.join([sampleName, 'pup']),
            "indel": outpath + '.'.join([sampleName, 'idf']),
            "sv": outpath + '.'.join([sampleName, 'svf']),
            "cnv": [outpath+'.'.join([sampleName, 'ghs']), outpath+'.'.join([sampleName, 'cov'])]}


if __name__ == "__main__":
    absPath = os.path.abspath(os.path.dirname(sys.argv[0]))
    parser = Job.Runner.getDefaultArgumentParser()
    parser.add_argument('bam', nargs='+', help='input bams')
    parser.add_argument('ref', help='references')
    parser.add_argument('seg', help='segmentSize')
    parser.add_argument('--ccd', help='ccd')
    parser.add_argument('outpath', help='output path')
    parser.add_argument('sampleName', help='sample name')
    parser.add_argument('--version', type=argparse.FileType('r'))
    parser.add_argument('--volumes', type=argparse.FileType('r'))

    options = parser.parse_args()
    version = json.load(options.version)
    volumes = json.load(options.volumes)
    variants = ['cnv', 'indel', 'sv', 'snv']
    start_job = Job()
    gvc_pipeline(start_job, options.ref, options.seg, options.bam, options.outpath,
                 options.sampleName, version, volumes, variants, ccd=options.ccd)

    with Toil(options) as toil:
        if not toil.options.restart:
            toil.start(start_job)
        else:
            toil.restart()
