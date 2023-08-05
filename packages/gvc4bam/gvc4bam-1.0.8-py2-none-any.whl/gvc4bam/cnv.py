
from toil.common import Toil
from toil.job import Job

import os
import shutil
import docker

import itertools
import variant_interface


from runner.runner import docker_runner, decorator_wrapt, docker_runner_method


class cnv(Job):

    def __init__(self, group_name, input_ghs, input_cov, outpath, sample_list, input_dirname, image, volumes, enable_panel, *args, **kwargs):
        sample_names = ','.join(sample_list[1:])
        self.image = image
        self.volumes = volumes
        if enable_panel:
            self.commandLine = ['sh', '/usr/local/bin/Panel/GVC_CNV_R.sh', input_ghs,
                                input_cov, sample_names, input_dirname]
        else:
            self.commandLine = ['GVC_CNV_R.sh', input_ghs,
                                input_cov, sample_names, input_dirname]
        self.sample_list = sample_list[1:]
        #self.suffixes = ['.CBS', '.cnv.bandAnn.xls', '.cnv.geneAnn.xls',
        #                 '.cnv.xls', '.correctedMutAF.LRR.pdf']
        self.suffixes = ['.cnv.geneAnn.xls']
        self.outpath = outpath
        self.input_dirname = input_dirname
        self.group_name = group_name
        self.suffixes_output = False if enable_panel else True
        super(cnv, self).__init__(*args, **kwargs)
        vd = variant_interface.VariantInterface()
        if  enable_panel :
            vd.set_cnv(os.path.join(self.outpath,self.group_name+'.cnv.simp'))
        else:
            vd.set_cnv(os.path.join(self.outpath,self.group_name+'.cnv.simp'),os.path.join(self.outpath,group_name+self.suffixes[0]))

    def run(self, fileStore):
        client = docker.from_env()
        docker_runner_method(self, self.commandLine,
                             "cnv", self.image, self.volumes)

        if self.suffixes_output:
            for  suffix in self.suffixes:
                sample_name = self.sample_list[0]
                shutil.move(os.path.join(self.input_dirname,
                                         sample_name+suffix), os.path.join(self.outpath, self.group_name+suffix))

        for sample_name in self.sample_list:
            shutil.move(self.input_dirname + '/' +
                        sample_name+'.cnv.simp', self.outpath+'/'+self.group_name+'.cnv.simp')


def cmdPhaser():
    parser = Job.Runner.getDefaultArgumentParser()
    parser.add_argument("ghs")
    parser.add_argument("cov")
    parser.add_argument("sample", nargs="+")
    parser.add_argument("input_dirname")
    parser.add_argument("outpath")
    return parser.parse_args()


if __name__ == "__main__":
    options = cmdPhaser()

    volumes = {
        "/disk": {
            "bind": "/disk",
            "mode": "rw"
        }
    }
    image = "cnv:1.0"
    start_job = cnv(options.ghs, options.cov, options.outpath, options.sample,
                    options.input_dirname, image, volumes)

    with Toil(options) as toil:
        if not toil.options.restart:
            toil.start(start_job)
        else:
            toil.restart()
