#!/usr/bin/python
import sys
import argparse
import pysam

def cmdPhase():
    parser = argparse.ArgumentParser(description = 'load and check Bam')
    parser.add_argument('reference',help='reference filename ')
    parser.add_argument('input_bam', help='input bed filename ')
    return parser.parse_args()

# check chr of bam and ref
def bamRefCheck( refFn , bamFn):
   # print refFn,bamFn
    bamFile = pysam.AlignmentFile(bamFn)
    #print bamFile.references
    fastaFile = pysam.FastaFile(refFn)
   # print fastaFile.references
   # print "bam:",bamFile.references
   # print "header",fastaFile.references
    return tuple(bamFile.references) ==  tuple(fastaFile.references)
# check bam.bai
def bamBai(bamFn):
    try:
        f = open(bamFn + '.bai')
        f.close()
    except Exception as E:
        print E
        sys.exit(-1)
if __name__ == '__main__':
    args = cmdPhase()
    bamRefCheck(args.reference, args.input_bam)
    bamBai(args.input_bam)
