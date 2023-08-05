#!/usr/bin/python
import sys
import argparse
import pysam


def cmdPhase():
    parser = argparse.ArgumentParser(description='Sort BedFile and Get BedReg')
    parser.add_argument('reference', help='reference filename ')
    parser.add_argument('input_bed', help='input bed filename ')
    parser.add_argument('output_bed', help='output bed filename')
    return parser.parse_args()


def loadReference(filename):
    try:
        fasta = pysam.FastaFile(filename)
    except ValueError as E:
        print 'if index file is missing'
        sys.exit(-1)
    except IOError as E:
        print 'if file could not be opened ', filename
        sys.exit(-1)
    return fasta


def fetchBedLines(filename, reference_name):
    bedLines = []
    with open(filename) as F:
        for line in F:
            Lines = line.strip('\n').split('\t')
            if len(Lines) < 3:
                print('Bed file format error. Please make sure the bed file is tab delimited.\
                     For more info on bed file format, please check out {}'.format(filename))
                sys.exit(-1)
            if Lines[0] not in reference_name:
                #Lines[0] = Lines[0].replace('chr','')
                # if Lines[0]  not in reference_name :
                print ('Chromosome name in bed file is different from reference.\
                    Check {} for correct chromosome names.'.format(filename))
                sys.exit(-1)
            Lines = Lines[0:3]
            bedLines.append(Lines)
    return bedLines


def bedSort_run(reference, input_bed, output_bed):
    fasta = loadReference(reference)
    references = dict((value, key)
                      for key, value in enumerate(fasta.references))

    with open(output_bed, 'w') as F:
        for item in sorted(fetchBedLines(input_bed, fasta.references), key=lambda x: (references[x[0]], int(x[1]))):
            F.write('\t'.join(item)+'\n')
    return None


def write_bed_reg(bedFile, outputFile):
    with open(bedFile, 'r') as F:
        chr_sum = []
        chr_name = []
        for bedline in F:
            dataList = bedline.strip('\n').split('\t')
            if len(chr_name) == 0:
                sum_base = int(dataList[2]) - int(dataList[1])
                chr_name.append(dataList[0])
            elif chr_name[-1] != dataList[0]:
                chr_sum.append(sum_base)
                sum_base = int(dataList[2]) - int(dataList[1])
                chr_name.append(dataList[0])
            else:
                sum_base = sum_base + int(dataList[2]) - int(dataList[1])
        chr_sum.append(sum_base)
    # print outputFile
    with open(outputFile, 'w') as F:
        F.write('#1.0-5-gd74ff94' + '\n')
        for item in zip(chr_name, chr_sum):
            F.write(item[0] + '\t' + str(item[1]) + '\n')
# check bed, sort bed and get bed.reg


def bed_check_sort_reg(ref, input_bed, sort_bed):
    fasta = loadReference(ref)
    references = dict((value, key)
                      for key, value in enumerate(fasta.references))
    with open(sort_bed, 'w') as F:
        for item in sorted(fetchBedLines(input_bed, fasta.references),
                           key=lambda x: (references[x[0]], int(x[1]))):
            F.write('\t'.join(item) + '\n')
    write_bed_reg(sort_bed, sort_bed + '.reg')


if __name__ == '__main__':

    args = cmdPhase()
    #fasta = loadReference(args.reference)

    #references = dict((value,key) for key,value in enumerate(fasta.references))
    # with open(args.output_bed,'w') as F:
    #    for item  in  sorted(fetchBedLines(args.input_bed,fasta.references),key=lambda x:(references[x[0]], int(x[1]))):
    #        F.write('\t'.join(item)+'\n')
    #write_bed_reg(args.output_bed, args.output_bed + '.reg')
    bed_check_sort_reg(args.reference, args.input_bed, args.output_bed)
