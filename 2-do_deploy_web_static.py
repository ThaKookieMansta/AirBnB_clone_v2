#!/usr/bin/python3
# Fabfile to distribute an archive to a web server.
import os.path
from datetime import datetime

from fabric.api import env, put, run, local


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
    try:
        if not os.path.exists(archive_path):
            return False

        archive_name = os.path.basename(archive_path)
        release_dir = '/data/web_static/releases'
        current_dir = '/data/web_static/current'

        put(archive_path, "/tmp")
        run("mkdir -p {}/{}".format(
            release_dir, archive_name.replace('.tgz', '')))
        run("tar -xzf /tmp/{} -C {}/{}".format(
            archive_name, release_dir, archive_name.replace('.tgz', '')))
        run("rm /tmp/{}".format(archive_name))
        run("mv {}/{}/web_static/* {}/{}".format(
            release_dir, archive_name.replace('.tgz', ''), release_dir,
            archive_name.replace('.tgz', '')))
        run("rm -rf {}/{}/web_static".format(
            release_dir, archive_name.replace('.tgz', '')))
        run("rm -rf {}".format(current_dir))
        run("ln -s {}/{} {}".format(
            release_dir, archive_name.replace('.tgz', ''), current_dir))
        print('New version deployed!')
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
