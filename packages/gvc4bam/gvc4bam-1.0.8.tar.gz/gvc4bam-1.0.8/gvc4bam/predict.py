from toil.common import Toil
from toil.job import Job

import pwd
import getpass
import docker
import functools
import itertools
import commands
import os
import time
import re
import json
import shutil
from collections import OrderedDict
from collections import defaultdict

from runner.runner import docker_runner, decorator_wrapt

import variant_interface

class MarkErrorPattern(Job):

    @decorator_wrapt
    def __init__(self, filter_file, xgboost_file, tumor_bam ,reference ,output_file ,sampleID ,variant, image, volumes,*args,**kwargs):
        self.image = image
        self.volumes = volumes
        self.commandLine = ['sh','/bin/tr_hdr.sh',filter_file,xgboost_file,tumor_bam,reference,output_file,sampleID,variant.upper()]
        super(MarkErrorPattern,self).__init__(*args,**kwargs)

    @docker_runner('MarkErrorPattern')
    def run(self, fileStore):
        return self.commandLine

class LinearPredict(Job):

    @decorator_wrapt
    def __init__(self, inputfile, outfile, json_file, model, image, volumes, *args,
                 **kwargs):
        self.inputfile = inputfile
        self.outfile = outfile
        self.setting_json = json_file
        self.model = model
        self.image = image
        self.volumes = volumes
        self.commandLine = [self.setting_json,
                            self.model, self.inputfile, self.outfile]
        #print(' '.join(self.commandLine))
        super(LinearPredict, self).__init__(*args, **kwargs)

    @docker_runner('LinearPredict')
    def run(self, fileStore):
        return self.commandLine


class XGBoostPredict(Job):

    @decorator_wrapt
    def __init__(self, inputfile, outfile, json_file, xml, modelPath, image, volumes, threads='1', *args, **kwargs):
        self.commandLine = ['gvc_pre.py', inputfile,
                            outfile, json_file, xml, modelPath]

        self.image = image
        self.volumes = volumes
        super(XGBoostPredict, self).__init__(*args, **kwargs)

    @docker_runner('XGBoostPredict')
    def run(self, fileStore):
        return self.commandLine


class BedFilter(Job):

    @decorator_wrapt
    def __init__(self, variant, mutantType, inputfile, bed, bam,image, volumes, *args, **kwargs):
        self.variant = variant
        self.mutantType = mutantType
        self.inputfile = inputfile
        self.bed = bed
        self.image = image
        self.volumes = volumes

        self.commandLine = ['/usr/bin/filter.sh',
                            inputfile, bed, mutantType + '_' + variant,bam]
        super(BedFilter, self).__init__(*args, **kwargs)

    @docker_runner('BedFilter')
    def run(self, fileStore):
        return self.commandLine


choice_vcf_dict = {
    'Somatic': {
        'snv': 'pup2vcf-somatic.pl',
        'indel': 'idf2vcf-somatic.pl',
        'sv': 'sv2vcf-somatic.pl'
    },
    'Germline': {
        'snv': 'pup2vcf-germline.pl',
        'indel': 'idf2vcf-germline.pl',
        'sv': 'sv2vcf-germline.pl'
    }
}
class PostProcessVCF(Job):
    @decorator_wrapt
    def __init__(self,variant, mutantType,inputfile,sample_name,output_vcf,bam,image, volumes, *args, **kwargs):
        self.image = image
        self.volumes = volumes
        self.commandLine = ['gvc2vcf.py',variant,mutantType,sample_name,inputfile,output_vcf,bam]
        super(PostProcessVCF,self).__init__(*args, **kwargs)

    @docker_runner('PostProcessVCF')
    def run(self, fileStore):
        return self.commandLine
    
class GenerateVCF(Job):
    @decorator_wrapt
    def __init__(self, variant, mutantType, inputfile, vcf_file_name, group_name, image, volumes,*args, **kwargs):
        self.variant = variant
        self.mutantType = mutantType
        self.inputfile = inputfile
        self.vcf_file_name = vcf_file_name
        self.group_name = group_name
        self.image = image
        self.volumes = volumes
        self.commandLine = [choice_vcf_dict[self.mutantType]
                            [self.variant], group_name, inputfile, vcf_file_name]
        super(GenerateVCF, self).__init__(*args, **kwargs)

    @docker_runner('GenerateVCF')
    def run(self, fileStore):
        return self.commandLine

class tmp_rm(Job):
    def __init__(self, group_name, outputPath, variants, models, strategy, mutantTypes, rm_predict, bed=None, *args, **kwargs):
        self.group_name = group_name
        self.outputPath = outputPath
        self.variants = variants
        self.models = models
        self.strategy = strategy
        self.mutantTypes = mutantTypes
        self.rm_predict = rm_predict
        self.bed = bed
        super(tmp_rm, self).__init__(*args, **kwargs)

    def run(self, fileStore):
        shutil.rmtree(os.path.join(self.outputPath, 'tmp'))
        if self.bed:
            os.remove(self.outputPath + '/' +
                      os.path.basename(self.bed) + '.sort')
            os.remove(self.outputPath + '/' +
                      os.path.basename(self.bed) + '.sort.reg')


def post_filter(root,predict_dict,variants,reference,tumor_bam,sample_name,output_path,version,volumes):
    #print (predict_dict)
    vd = variant_interface.VariantInterface()
    for variant in variants:
        MarkErrorPath =  os.path.join(os.path.dirname(predict_dict[variant]['filter']),'.'.join([sample_name,'errorpattern',variant]))
        if 'xgboost' in  predict_dict[variant].keys():
            markJob = MarkErrorPattern(predict_dict[variant]['filter'],predict_dict[variant]['xgboost'],tumor_bam,reference,MarkErrorPath,sample_name,variant,version['postgvc'], volumes)
        else:
            markJob = MarkErrorPattern(predict_dict[variant]['filter'],predict_dict[variant]['grig'],tumor_bam,reference,MarkErrorPath,sample_name,variant,version['postgvc'], volumes)
        root.addChild(markJob)
        vcfPath = os.path.join(output_path,'.'.join([sample_name,'Somatic',variant,'vcf']))
        postJob = PostProcessVCF(variant,'Somatic',MarkErrorPath,sample_name,vcfPath,tumor_bam,version['gvc2vcf'],volumes)
        vd.set_vcf(variant,'Somatic',vcfPath)
        markJob.addChild(postJob)

def Predict_pipeline(root, group_name, sampleList, outputPath, infoDict, inputfileDict, variants, sequenceTypes, strategy, mutantTypes, bed, models, xml, modelPath, bam,version, volumes):

    predict_dict = defaultdict(type(defaultdict()))
    # print variants, models, mutantTypes
    for variant, model, mutantType in itertools.product(variants, models, mutantTypes):
        # print simpleName
        inputfile = inputfileDict[variant]
        dirname = os.path.dirname(inputfile)
        json_file = infoDict[variant][mutantType]
        sample_name = '.'.join(
            [group_name, model, strategy, mutantType, variant])
        filter_path = dirname + '/' + sample_name
        output_sample_name = outputPath + '/' + sample_name

        predictJob = None
        if model == 'filter' and mutantType == 'Germline':
            continue
        # and not(variant == 'indel' and mutantType == 'Somatic')
        if model == 'xgboost' and (variant != 'sv'):
            predictJob = XGBoostPredict(inputfile, filter_path, json_file, xml,
                                        modelPath, version['xgboost'], volumes, cores='10', memory="20G")
        if model != 'xgboost':
            predictJob = LinearPredict(inputfile, filter_path, json_file, model,
                                       version['filter'], volumes)

        if predictJob is None:
            continue
        root.addChild(predictJob)

        if model == 'filter' and mutantType == 'Somatic':
            vcf_file_name = os.path.join(outputPath,'.'.join([group_name,mutantType, variant,'all','vcf']))
        else:
            vcf_file_name = os.path.join(outputPath,'.'.join([group_name,mutantType, variant,'pass','vcf']))
        if strategy == 'WES' or strategy == 'Panel_tissue':
            # bed filter
            bed_filterJob = BedFilter(
                variant, mutantType, filter_path, bed,bam, version['bed_filter'], volumes)
            predictJob.addChild(bed_filterJob)
            # TODO: After fixed BUGs(Indel post-process) , variant in ['snv','indel']
            if mutantType == 'Somatic' and  variant != 'sv':
                predict_dict[variant][model] = filter_path + ".bed.filter"
            else:
                vcfJob = GenerateVCF(variant, mutantType, filter_path + ".bed.filter",
                    vcf_file_name, group_name, version['gvc2vcf'], volumes)
                
                if model != 'filter':
                    vd = variant_interface.VariantInterface()
                    vd.set_vcf(variant,mutantType,vcf_file_name)
                bed_filterJob.addChild(vcfJob)       
        elif strategy == 'WGS':
            if mutantType == 'Somatic' and  variant != 'sv':
                predict_dict[variant][model] = filter_path
            else:
                vcfJob = GenerateVCF(variant, mutantType, filter_path, vcf_file_name, group_name,
                                        version['gvc2vcf'], volumes)
                predictJob.addChild(vcfJob)
                if model != 'filter':
                    vd = variant_interface.VariantInterface()
                    vd.set_vcf(variant,mutantType,vcf_file_name)
    return predict_dict

def tmp_rm_def(root, group_name, outputPath, variants, models, strategy, mutantTypes, rm_predict, bed):
    tmp_rmJob = tmp_rm(group_name, outputPath, variants,
                       models, strategy, mutantTypes, rm_predict, bed)
    root.addChild(tmp_rmJob)


if __name__ == "__main__":

    absPath = os.path.abspath(os.path.dirname(__file__))
    parser = Job.Runner.getDefaultArgumentParser()
    parser.add_argument('sample_name')
    parser.add_argument('input_dir')
    parser.add_argument('reference')
    parser.add_argument('bam')
    parser.add_argument('output')
    parser.add_argument(
        '--gvc_lib',
        help="The library folder has configuration file." + '\n' +
             'The docker volume file needs to be modified. ' +
             'A dictionary to configure volumes mounted inside the container. ' +
             'The key is either the host path or a volume name, ' +
             'and the value is a dictionary with the keys:' + '\n' +
             'bind: The path to mount the volume inside the container' +
             '(the host path need same with the container path).' + '\n' +
             'mode: rw to mount the volume read/write.' + '\n' +
             'eg: {"/disk": {"bind": "/disk","mode": "rw"}}"',
        default=absPath + '/../gvc_lib/')
    options = parser.parse_args()


    input_gvcs = dict()
    variant = set()
    infoDict = defaultdict(type(defaultdict()))
    mutantTypes = set()
    for filename in os.listdir(options.input_dir):
        if re.search("\.json$", filename):
            with open(os.path.join(options.input_dir, filename)) as F:
                setting = json.load(F)
                if 'variant' in setting:
                    infoDict[setting['variant']][setting['mutantTypes']
                                                 ] = os.path.join(options.input_dir, filename)
                    variant.add(setting['variant'])
                    sequenceTypes = setting['sequenceType']
                    strategy = setting['strategy']
                    mutantTypes.add(setting['mutantTypes'])
        re_gvcs = re.search(options.sample_name+'.(idf|pup|svf)', filename)

        if re_gvcs:

            if re_gvcs.group(1) == 'idf':
                input_gvcs['indel'] = os.path.join(options.input_dir, filename)
            elif re_gvcs.group(1) == 'svf':
                input_gvcs['sv'] = os.path.join(options.input_dir, filename)
            else:
                input_gvcs['snv'] = os.path.join(options.input_dir, filename)

    for filename in os.listdir(os.path.dirname(options.input_dir)):
        if re.search('bed', filename):
            bed = os.path.join(os.path.dirname(options.input_dir), filename)

    gvc_lib = options.gvc_lib
    volumes = {
        "/disk": {
            "bind": "/disk",
            "mode": "rw"
        }
    }
    print("****** loading paramter from template files ******")
    print(sequenceTypes, strategy)
    print(input_gvcs)
    print(infoDict)
    print(variant)
    print(bed)
    print(gvc_lib)

    models = ['filter','grig','xgboost']
    version_path = gvc_lib + '/version.json'
    volumes_path = gvc_lib + '/volumes.json'
    thread_path = gvc_lib + '/thread.json'
    xml_path = gvc_lib + '/format.xml'
    model_path = gvc_lib + '/Model/PE150'

    with open(volumes_path, 'r') as f:
        volumes = json.load(f, object_pairs_hook=OrderedDict)

    with open(version_path, 'r') as verf:
        version = json.load(verf)

    with open(thread_path, 'r') as thref:
        thread = json.load(thref)

    start_job = Job()

    dummy_job = Job()

    outputPath = options.output
    predict_dict = Predict_pipeline(start_job,options.sample_name,['N','T'],outputPath,infoDict,input_gvcs,variant,sequenceTypes,strategy,mutantTypes,bed,models,xml_path,model_path,options.bam,version,volumes)
    start_job = start_job.encapsulate()
    post_filter(start_job,predict_dict,['snv'],options.reference,options.bam,options.sample_name,outputPath,version,volumes)
    
    with Toil(options) as toil:
        if not toil.options.restart:
            toil.start(start_job)
        else:
            toil.restart()