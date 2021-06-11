from __future__ import print_function

import argparse
import socket
import os
import sys
from datetime import datetime

from ssh2.session import Session
from ssh2.sftp import LIBSSH2_FXF_READ, LIBSSH2_FXF_CREAT, LIBSSH2_FXF_WRITE, LIBSSH2_SFTP_S_IRUSR, LIBSSH2_SFTP_S_IRGRP, LIBSSH2_SFTP_S_IWUSR, LIBSSH2_SFTP_S_IROTH

import config

#config
USERNAME = config.USERNAME
PASSWORD = config.PASSWORD
SERVER = config.SERVER
PORT = config.PORT
SERVER_DIR_TREE_LOCATION = config.SERVER_DIR_TREE_LOCATION
SOURCE_DIR_LOCATION = config.SOURCE_DIR_LOCATION

session = Session()

def scpTransfer(session):
    fileinfo = os.stat(SOURCE_DIR_LOCATION) #CHANGE THIS FOR RECURSIVE DIRECTORY LISTING. RN THIS JUST DOES ONE SPECIFIC FILE.
    
    try:
        channel = session.scp_send64(SERVER_DIR_TREE_LOCATION, fileinfo.st_mode & 0o777, fileinfo.st_size, fileinfo.st_mtime, fileinfo.st_atime)

        print("Starting SCP of local file %s to remote %s:%s" % (SOURCE_DIR_LOCATION, SERVER, SERVER_DIR_TREE_LOCATION))
    
        try:    
            with open(SOURCE_DIR_LOCATION, 'rb') as local_fh:
                for data in local_fh:
                    channel.write(data)
        except Exception as e:
            print(str(e))
    except Exception as e:
        print(str(e))

def sftpGet(sftp, session):    
    try:
        with sftp.open(SOURCE_DIR_LOCATION, LIBSSH2_FXF_READ, LIBSSH2_SFTP_S_IRUSR) as remote_fh, open(SERVER_DIR_TREE_LOCATION, 'wb') as local_fh:
            for _, data in remote_fh:
                local_fh.write(data)
    except Exception as e:
        print("Error at sftpRead: ", str(e))

def sftpSend(sftp, session):
    mode = LIBSSH2_SFTP_S_IRUSR | LIBSSH2_SFTP_S_IWUSR | LIBSSH2_SFTP_S_IRGRP | LIBSSH2_SFTP_S_IROTH
    flags = LIBSSH2_FXF_CREAT | LIBSSH2_FXF_WRITE
    
    print("Starting copy of local file %s to remote %s:%s" % (SOURCE_DIR_LOCATION, SERVER, SERVER_DIR_TREE_LOCATION))
    
    try:
        with open(SOURCE_DIR_LOCATION, 'rb') as local_fh, sftp.open(SERVER_DIR_TREE_LOCATION, flags, mode) as remote_fh:
            for data in local_fh:
                remote_fh.write(data)
    except Exception as e:
        print("Error at sftpRead: ", str(e))
    


def initialise():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER, int(PORT)))
    session = Session()
    session.handshake(sock)
    session.userauth_password(USERNAME, PASSWORD)
    sftp = session.sftp_init()
    return sftp

def mkdir_p(sftp, remote, is_dir=False):
    # emulates mkdir_p if required. 
    dirs = []
    dir, basename = os.path.split(remote)
    while len(dir) > 1:
        dirs.append(dir)
        dir, _  = os.path.split(dir)

    if len(dir) == 1 and not dir.startswith("/"): 
        dirs.append(dir) # For a remote path like y/x.txt 

    while len(dirs):
        dir = dirs.pop()
        try:
            sftp.stat(dir)
        except:
            print("making ... dir",  dir)
            sftp.mkdir(dir, 0o777)

sftp = initialise()
mkdir_p(sftp, "/Pokemon/Doraemon")