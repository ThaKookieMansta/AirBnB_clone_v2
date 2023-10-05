#!/usr/bin/python3
# This function generates an archive from the web static content.
import os.path
from datetime import datetime
from fabric.api import local, env

env.user = 'ubuntu'
env.hosts = ['34.227.93.59', '18.234.192.168']


def do_pack():
    """
    This function generates an archive from the web static content
    Returns:

    """
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    file = "versions/web_static_{}.tgz".format(current_time)
    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
    if local("tar -cvzf {} web_static".format(file)).failed is True:
        return None
    return file
