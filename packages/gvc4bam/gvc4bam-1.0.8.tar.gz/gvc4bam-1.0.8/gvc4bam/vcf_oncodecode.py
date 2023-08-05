from toil.common import Toil
from toil.job import Job
from collections import OrderedDict

import pwd
import getpass
import argparse
import os
import sys
import json
import docker
import itertools
import time
from runner.runner import docker_runner, decorator_wrapt, docker_runner_method


class Annotation(Job):

    def __init__(self, inputfile, outpath, sampleName, image, volumes, *args, **kwargs):
        self.inputfile = inputfile
        self.outpath = outpath
        self.sampleName = sampleName
        self.image = image
        self.volumes = volumes

        self.commandLine = ['bash', '/usr/local/bin/OncoDecode.sh',
                            self.inputfile, self.outpath, self.sampleName]
        super(Annotation, self).__init__(*args, **kwargs)

    def run(self, fileStore):
        client = docker.from_env()
        lines = open(self.inputfile, 'r').readlines()
        l_n = 0
        for line in lines:
            if line[0] == "#":
                continue
            else:
                l_n = l_n + 1
        if l_n > 0:
            docker_runner_method(self, self.commandLine,
                                 "Annotation", self.image, self.volumes)
        else:
            self.log(self.inputfile +
                     ' has less than 1 mutation pos, so do not run oncodecode')


def cmd_parser(absPath):
    parser = Job.Runner.getDefaultArgumentParser()
    parser.add_argument('--inputfile', help="vcf mutation file"),
    parser.add_argument('--outpath', help='The output folder'),
    parser.add_argument('--sampleName', help='sample name'),
    parser.add_argument('--version', type=argparse.FileType('r'))
    parser.add_argument('--volumes', type=argparse.FileType('r'))
    return parser.parse_args()


def vcf_oncodecode_fun(root, inputfile, outpath, sampleName, version, volumes):
    job = Annotation(inputfile, outpath, sampleName,
                     version['vcf_oncodecode'], volumes)
    root.addChild(job)


def run_vcf_oncodecode(root, outpath, group_name, variants, models, mutantTypes, strategy, version, volumes):
    for variant, model, mutantType in itertools.product(variants, models, mutantTypes):
        if model == 'xgboost' and variant == 'snv' and mutantType == 'Somatic':
            inputfile = outpath + '/' + group_name + '.xgboost.' + \
                strategy + '.' + mutantType + '.' + variant + '.pass.vcf'
            job = Annotation(inputfile, outpath, group_name,
                             version['vcf_oncodecode'], volumes)
            root.addChild(job)


if __name__ == "__main__":
    absPath = os.path.abspath(os.path.dirname(sys.argv[0]))
    options = cmd_parser(absPath)
    inputfile = options.inputfile
    outpath = options.outpath
    sampleName = options.sampleName
    version = json.load(options.version, object_pairs_hook=OrderedDict)
    volumes = json.load(options.volumes, object_pairs_hook=OrderedDict)
    start_job = Job()
    vcf_oncodecode_fun(start_job, inputfile, outpath,
                       sampleName, version, volumes)

    with Toil(options) as toil:
        if not toil.options.restart:
            toil.start(start_job)
        else:
            toil.restart()
