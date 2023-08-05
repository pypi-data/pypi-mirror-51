
import shutil
import re
from toil.common import Toil
from toil.job import Job
import docker

import pwd
import getpass
import sys
import os
import itertools
import argparse
import json
import time

from collections import defaultdict, OrderedDict
from runner.runner import docker_runner, decorator_wrapt, docker_runner_method


class QC_DefineRegion(Job):
    @decorator_wrapt
    def __init__(self, ref, bed, strategy, image, volumes, *args, **kwargs):
        self.ref = ref
        self.bed = bed
        self.strategy = strategy
        self.image = image
        self.volumes = volumes
        if strategy == 'WGS':
            self.commandLine = [
                'python', '/usr/local/bin/rootUpdate.py', self.ref, '--seqtype', self.strategy]
        elif strategy == 'WES' or strategy == 'Panel_tissue':
            self.commandLine = ['python', '/usr/local/bin/rootUpdate.py',
                                self.ref, '--input_bed', self.bed, '--seqtype', self.strategy]
        super(QC_DefineRegion, self).__init__(*args, **kwargs)

    @docker_runner("QC_DefineRegion")
    def run(self, fileStore):
        return self.commandLine


def rootUpdateJob_pipeline(root, ref, bed, strategy, version, volumes):
    rootUpdate_job = QC_DefineRegion(
        ref, bed, strategy, version['gvcqc'], volumes)
    root.addChild(rootUpdate_job)


class QC(Job):
    @decorator_wrapt
    def __init__(self, volumes, image, config, *args, **kwargs):
        self.volumes = volumes
        self.image = image
        self.command = ['bam2qc.py', config]
        super(QC, self).__init__(*args, **kwargs)

    @docker_runner('QC')
    def run(self, fileStore):
        return self.command


def qc_config(output_name, strategy, l_bam_path, l_bam_names, reference, bed, sample_name):

    config_dict = dict()
    if not isinstance(l_bam_names, list):
        raise ValueError("l_bam_name must be list type")
    config_dict['bam_name'] = l_bam_names
    config_dict['sample_id'] = sample_name

    if not isinstance(l_bam_path, list):
        raise ValueError("l_bam_path must be slist type")
    config_dict['bam'] = l_bam_path
    if re.search('panel', strategy, re.I) or strategy == 'WES':
        config_dict['bed'] = bed
    else:
        config_dict['reference'] = reference
    config_dict['outpath'] = output_name
    config_dict['enable_error_flags'] = "False"
    return config_dict


def qc_pipeline(root, tmp_path, output_name, strategy, l_bam_path, l_bam_names, reference, bed, sample_name, version, volumes):
    config_dict = qc_config(output_name, strategy, l_bam_path,
                            l_bam_names, reference, bed, sample_name)
    qc_config_file = os.path.join(tmp_path, 'qc_config.json')
    with open(qc_config_file, 'w') as config_f:
        json.dump(config_dict, config_f)
    qcjob = QC(volumes,
               version['gvcqc'], qc_config_file,cores=3)
    root.addChild(qcjob)
    return map(lambda x: os.path.join(output_name, x, 'QC.txt'), l_bam_names)


class QC_Postprocess(Job):
    @decorator_wrapt
    def __init__(self, txt_list, outfile, sequenceType, strategy, variant, mutantType, sample_name, image, volumes, *args, **kwargs):
        self.commandLine = ['predictJson.py']
        self.commandLine.extend(txt_list)
        self.commandLine.extend(
            [outfile, sequenceType, strategy, variant, mutantType, ','.join(sample_name)])
        self.image = image
        self.volumes = volumes
        super(QC_Postprocess, self).__init__(*args, **kwargs)

    @docker_runner("QC_Postprocess")
    def run(self, fileStore):
        return self.commandLine


class rmQCtemp(Job):
    def __init__(self, l_dirs, *args, **kwargs):
        self.l_dirs = map(os.path.dirname, l_dirs)
        super(rmQCtemp, self).__init__(*args, **kwargs)

    def run(self, fileStore):
        for dir_name in self.l_dirs:
            shutil.rmtree(dir_name)


def qc2predict(root, qc_txts, output_path, samples, sequenceType, strategy, variants, mutantTypes, version, volumes):
    json_dict = defaultdict(type(defaultdict(str)))
    for variant, mutantType in itertools.product(variants, mutantTypes):
        outfile = output_path + '/' + \
            '.'.join([sequenceType, strategy, variant, mutantType, 'json'])
        json_dict[variant][mutantType] = outfile
        jsonJob = QC_Postprocess(qc_txts, outfile, sequenceType,
                                 strategy, variant, mutantType, samples, version['gvcqc'], volumes)
        root.addChild(jsonJob)
    #rmQC = rmQCtemp(qc_txts)
    #root.addFollowOn(rmQC)
    return json_dict


def cmdPhaser(absPath):
    parser = Job.Runner.getDefaultArgumentParser()
    parser.add_argument("tmp", help="tmp path")
    parser.add_argument('output_path', help="output path")
    parser.add_argument('bam', nargs='+', help="bam")
    parser.add_argument("sample_name", help="sample name")
    parser.add_argument(
        '--strategy', choices=['WES', 'WGS', 'Panel_tissue'])
    parser.add_argument("--bamname", action='append', help="bam name")
    parser.add_argument(
        '--reference', help="input reference file"
    )
    parser.add_argument(
        "--bed", help="bed file"
    )
    parser.add_argument(
        '--seqtype', choices=['Hiseq', 'CN500', 'Novaseq'], default='Hiseq')
    parser.add_argument(
        '--filtermodel', choices=['xgboost', 'filter', 'empirical', 'grig'], metavar='model', action='append', default=[])
    parser.add_argument(
        '--mutantType', choices=['Somatic', 'Germline'], action='append', default=[])
    parser.add_argument(
        '--version', type=argparse.FileType('r'), required=True)
    parser.add_argument(
        '--volumes', type=argparse.FileType('r'), required=True)

    return parser.parse_args()


if __name__ == "__main__":
    absPath = os.path.abspath(os.path.dirname(sys.argv[0]))
    options = cmdPhaser(absPath)
    version = json.load(options.version)
    volumes = json.load(options.volumes)
    start_job = Job()

    qc_txts = qc_pipeline(start_job, options.tmp, options.output_path, options.strategy,
                          options.bam, options.bamname,
                          options.reference, options.bed, options.sample_name, version, volumes)

    start_job = start_job.encapsulate()

    variants = ['snv', 'indel']
    qc2predict(start_job, qc_txts, options.output_path, options.sample_name, options.seqtype, options.strategy,
               variants, options.mutantType, version, volumes)

    with Toil(options) as toil:
        if not toil.options.restart:
            toil.start(start_job)
        else:
            toil.restart()
