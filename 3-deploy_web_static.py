#!/usr/bin/python3
# This script creates and distributes an archive to the web servers
import os.path
from datetime import datetime
from fabric.api import env, local, put, run

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


def do_deploy(archive_path):
    """
    This function distributes an archive to servers
    Args:
        archive_path:

    Returns:

    """
    if os.path.isfile(archive_path) is False:
        return False
    file = archive_path.split("/")[-1]
    name = file.split(".")[0]

    if put(archive_path, "/tmp/{}".format(file)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/".
                   format(name)).failed is True:
        return False
    if run("mkdir -p /data/web_static/releases/{}/".
                   format(name)).failed is True:
        return False
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
                   format(file, name)).failed is True:
        return False
    if run("rm /tmp/{}".format(file)).failed is True:
        return False
    if run("mv /data/web_static/releases/{}/web_static/* "
           "/data/web_static/releases/{}/".format(name, name)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/web_static".
                   format(name)).failed is True:
        return False
    if run("rm -rf /data/web_static/current").failed is True:
        return False
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
                   format(name)).failed is True:
        return False
    return True


def deploy():
    """
    This function creates and distributes an archive to the web servers
    Returns:

    """
    file = do_pack()
    if file is None:
        return False
    return do_deploy(file)
