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
    try:
        archive = archive_path.split('/')[-1]
        path = '/data/web_static/releases/' + archive.strip('.tgz')
        current = '/data/web_static/current'
        put(archive_path, '/tmp')
        run('mkdir -p {}/'.format(path))
        run('tar -xzf /tmp/{} -C {}'.format(archive, path))
        run('rm /tmp/{}'.format(archive))
        run('mv {}/web_static/* {}'.format(path, path))
        run('rm -rf {}/web_static'.format(path))
        run('rm -rf {}'.format(current))
        run('ln -s {} {}'.format(path, current))
        print('New version deployed!')
        return True
    except FileNotFoundError:
        return False


def deploy():
    """
    This function creates and distributes an archive to the web servers
    Returns:

    """
    archive_path = do_pack()
    answer = do_deploy(archive_path)
    return answer
