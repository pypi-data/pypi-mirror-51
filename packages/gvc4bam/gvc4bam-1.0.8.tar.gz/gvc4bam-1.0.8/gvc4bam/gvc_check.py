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
from runner.runner import docker_runner, decorator_wrapt


class GVC_check(Job):
    @decorator_wrapt
    def __init__(self, image, volumes, *args, **kwargs):
        self.image = image
        self.volumes = volumes

        self.commandLine = ['/usr/local/bin/gvcR']
        super(GVC_check, self).__init__(*args, **kwargs)

    @docker_runner('gvc_check')
    def run(self, fileStore):
        return self.commandLine
        # client = docker.from_env()
        # client.containers.run(
        #     self.image, self.commandLine, volumes=self.volumes, privileged=True, remove=True, user=pwd.getpwnam(getpass.getuser()).pw_uid)


def cmd_parser(absPath):
    parser = Job.Runner.getDefaultArgumentParser()
    parser.add_argument('--version', type=argparse.FileType('r'),
                        default=file(absPath + '/../etc/version.json'))
    parser.add_argument('--volumes', type=argparse.FileType('r'),
                        default=absPath + '/../etc/volumes.json')
    return parser.parse_args()


def gvc_check_fun(root, version, volumes):
    job = GVC_check(version['gvc_check'], volumes)
    root.addChild(job)


if __name__ == "__main__":
    absPath = os.path.abspath(os.path.dirname(sys.argv[0]))
    options = cmd_parser(absPath)

    version = json.load(options.version, object_pairs_hook=OrderedDict)
    volumes = json.load(options.volumes, object_pairs_hook=OrderedDict)
    start_job = Job()
    gvc_check_fun(start_job, version, volumes)

    with Toil(options) as toil:
        if not toil.options.restart:
            toil.start(start_job)
        else:
            toil.restart()
