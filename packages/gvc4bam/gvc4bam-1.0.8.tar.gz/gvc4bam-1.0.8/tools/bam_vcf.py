#!/usr/bin/python
import argparse
import sys
import os
import subprocess
import time
import json
from collections import OrderedDict
import argparse


def QC_common_time(runtime, check_type, QC_types=['QC']):
    return map(lambda x: runtime[x][check_type], QC_types)


def QC_time_def(runtime):
    return QC_common_time(runtime, 'total')


def QC_thread_def(runtime):
    return QC_common_time(runtime, 'thread')


def cmdPhase(absPath):
    parser = argparse.ArgumentParser(description="Bam_Vcf")
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
        '--mutantType',
        help="Switch algorithm for germline or somatic mutation detection",
        choices=['Somatic', 'Germline'],
        required=True,
        action='append',
        default=[])
    parser.add_argument(
        '--region',
        help=argparse.SUPPRESS
    )
    parser.add_argument('--strategy', choices=['WES', 'Panel', 'WGS'],
                        help='Switch algorithm for WES, Panel or WGS analysis', required=True)
    parser.add_argument(
        '--sample_name', help="Name of the sample to be analyzed.", required=True)
    parser.add_argument('--CNV', action='store_true', default=False,
                        help='calculate and output CNV simultaneously')
    parser.add_argument('--SV', action='store_true', default=False,
                        help='calculate and output SV simultaneously')
    parser.add_argument(
        '--maxMemory', help="The maximum amount of memory to request from the batch" + '\n' +
        "system at any one time, eg: 32G.")
    parser.add_argument(
        '--maxCores', help="The maximum number of CPU cores to request from the batch" + '\n' +
        "system at any one time, eg: 8.")
    return parser.parse_args()
#


if __name__ == "__main__":
    absPath = os.path.abspath(os.path.dirname(sys.argv[0]))
    options = cmdPhase(absPath)
    # abspath = os.path.dirname(os.path.abspath(__file__)) + '/'
    commandLine = ['python', '-m', 'gvc4bam.gvc_vcf_pipeline', options.outpath + '/jobStore', options.input_json, options.reference,
                   options.outpath]

    if options.region:
        commandLine.extend(['--region', options.region])

    if options.CNV:
        commandLine.append('--CNV')

    if options.SV:
        commandLine.append('--SV')

    if options.dbsnp:
        commandLine.extend(['--dbsnp', options.dbsnp])
    if options.bed:
        commandLine.extend(['--bed', options.bed])
    if options.segmentSize:
        commandLine.extend(['--segmentSize', options.segmentSize])
    if options.maxMemory:
        commandLine.extend(['--maxMemory', options.maxMemory])
    if options.maxCores:
        commandLine.extend(['--maxCores', options.maxCores])

    for mutantType in options.mutantType:
        commandLine.extend(['--mutantType', mutantType])

    commandLine.extend(['--gvc_lib', options.gvc_lib, '--strategy', options.strategy, '--sample_name', options.sample_name, '--clean=never',
                        '--stats', '--rmtmp'])
    STDERR = open(options.outpath + '/logFile', 'w')
    Start_time = time.time()
    # print "Start_time:", Start_time

    proc1 = subprocess.Popen(commandLine, stderr=STDERR)

    if proc1.wait() != 0:
        with open(options.outpath + '/logFile') as flog:
            sys.stderr.writelines(flog.readlines())
            sys.exit(-3)
    cmd2 = ['python', absPath + '/check_runtime.py', options.outpath + '/logFile', options.outpath + '/jobStore',
            options.outpath + '/runtime.json']
    proc2 = subprocess.Popen(cmd2, stderr=STDERR)
    proc2.wait()
    End_time = time.time()
    # print "End_time:", End_time
    print "Runtime:", "".join([str(End_time - Start_time), '(s)'])
    with open(options.outpath + '/runtime.json') as fp:
        runtime = json.load(fp, object_pairs_hook=OrderedDict)
    QC_total_time = QC_time_def(runtime)
    QC_threads = QC_thread_def(runtime)
    print "GVC: ", "Threads:", runtime['GVC']['thread'], ",Total_time:", "".join(
        [str(runtime['GVC']['total']), '(s)'])
    print "QC: ", "Threads:", round(sum(
        QC_threads) / len(QC_threads)), ",Total_time:", "".join([str(sum(QC_total_time)), '(s)'])
    # if os.path.exists(options.outpath + '/logFile'):
    #     with open(options.outpath + '/logFile') as f:
    #         lines = f.readlines()
    #         for line in lines:
    #             if 'ERROR' in line or 'Error' in line:
    #                 print line
    if os.path.exists(options.outpath + '/runtime.json'):
        os.remove(options.outpath + '/runtime.json')
    if os.path.exists(options.outpath + '/logFile'):
        os.remove(options.outpath + '/logFile')
