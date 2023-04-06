#!/usr/bin/python3
# script that distributes an archive to web servers
from fabric.api import env, put, run, local
from os.path import exists, isdir
import os.path
import re


# Set the username and host for SSH connection to the server
env.user = 'ubuntu'
env.hosts = ['54.174.230.101', '100.26.57.164']
env.key_filename = '~/.ssh/id_rsa'


def do_deploy(archive_path):
    """
        Distributes archive to web servers
    """
    # Check if the archive file exists
    if not exists(archive_path):
        return False

    # Upload the archive to the /tmp/ directory of the web server
    put(archive_path, "/tmp/")

    # Uncompress the archive to the folder
    filename = re.search(r'[^/]+$', archive_path).group(0)
    folder = "/var/www/html/hbnb_static"

    # Create the folder if it doesn't exist
    if not exists(folder):
        run("mkdir -p {}".format(folder))

    # Extract files from archive
    run("tar -xzf /tmp/{} -C {}".format(filename, folder))

    # Remove archive from web server
    run("rm /tmp/{}".format(filename))

    print("New version deployed!")
    return True

# Usage:
# do_deploy('/path/to/archive.tar.gz')
