from toil.common import Toil
from toil.job import Job

from runner.runner import docker_runner, decorator_wrapt
import re
import docker


class verify_license(Job):
    @decorator_wrapt
    def __init__(self, image, volumes, *args, **kwargs):
        self.image = image
        self.volumes = volumes
        self.commandLine = ['check_license']
        return super(verify_license, self).__init__(*args, **kwargs)

    @docker_runner("verify_license")
    def run(self, fileStore):
        return self.commandLine


def get_license_status(gvc_lib, image):
    """Get GVC product license status.

    Args:
        gvc_lib: gvc_lib abosulte path (str type)
        image:  docker images like  xgboost:1.0-41-g9f68680

    Return:
    {
        "returnCode": 0,  0 or 1 
        "error_file":"gvc.lic",   gvc.lic or license.txt
        "error_msg":"output"
    }
    """
    client = docker.from_env()
    volumes = {
        gvc_lib: {
            "bind": "/Genowis",
            "mode": "rw"
        }
    }
    contains = client.containers.run(
        image, ['check_license'], network_mode='host', volumes=volumes, detach=True)

    stream = contains.logs(stream=True)
    buffer = ''.join(stream)
    if contains.wait() != 0:
        if re.search('license ERROR :', buffer):
            contains.remove(v=True)
            print ([buffer])
            error_msg = re.search(
                '(?<=license ERROR :\n)\s+(.*)\s+(?=\nthe pc signature is :)', buffer,re.MULTILINE).group(1)
            return {"returnCode": -1,
                    "error_file": "gvc.lic",
                    "error_msg": error_msg
                    }
        else:
            contains.remove(v=True)
            error_msg = buffer
            return {"returnCode": -1,
                    "error_file": "license.txt",
                    "error_msg": buffer.strip('\n')
                    }
    else:
        contains.remove(v=True)
        return {"returnCode": 0}
