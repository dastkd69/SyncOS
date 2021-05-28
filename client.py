from __future__ import print_function

import argparse
import socket
import os
import sys
from datetime import datetime

from ssh2.session import Session
from ssh2.sftp import LIBSSH2_FXF_READ, LIBSSH2_FXF_CREAT, LIBSSH2_FXF_WRITE, LIBSSH2_SFTP_S_IRUSR, LIBSSH2_SFTP_S_IRGRP, LIBSSH2_SFTP_S_IWUSR, LIBSSH2_SFTP_S_IROTH

import config

USERNAME = config.USERNAME
PASSWORD = config.PASSWORD
SERVER = config.SERVER
PORT = config.PORT

parser = argparse.ArgumentParser()

parser.add_argument('source', help="Source file to copy")
parser.add_argument('destination', help="Remote destination file to copy to")
parser.add_argument('--protocol', dest='protocol',default='SCP',help='Protocol to use')
parser.add_argument('--host', dest='host',default=SERVER, help='Host to connect to')
parser.add_argument('--port', dest='port', default=PORT, help="Port to connect on", type=int)
parser.add_argument('-u', dest='user', default=USERNAME, help="User name to authenticate as")

args = parser.parse_args()

def timer(now):
    taken = datetime.now() - now
    print("Finished writing remote file in %s" % (taken))

def scpTransfer(args, session):
    fileinfo = os.stat(args.source)
    now = datetime.now()
    try:
        channel = session.scp_send64(args.destination, fileinfo.st_mode & 0o777, fileinfo.st_size,fileinfo.st_mtime, fileinfo.st_atime)

        print("Starting SCP of local file %s to remote %s:%s" % (args.source, args.host, args.destination))
    
        try:    
            with open(args.source, 'rb') as local_fh:
                for data in local_fh:
                    channel.write(data)
        except Exception as e:
            print(str(e))
    except Exception as e:
        print(str(e))
    
    timer(now)

def sftpGet(args, session):
    sftp = session.sftp_init()
    now = datetime.now()
    
    try:
        with sftp.open(args.source, LIBSSH2_FXF_READ, LIBSSH2_SFTP_S_IRUSR) as remote_fh, open(args.destination, 'wb') as local_fh:
            for _, data in remote_fh:
                local_fh.write(data)
    except Exception as e:
        print("Error at sftpRead: ", str(e))

    timer(now)

def sftpSend(args, session):
    sftp = session.sftp_init()
    mode = LIBSSH2_SFTP_S_IRUSR | LIBSSH2_SFTP_S_IWUSR | LIBSSH2_SFTP_S_IRGRP | LIBSSH2_SFTP_S_IROTH
    flags = LIBSSH2_FXF_CREAT | LIBSSH2_FXF_WRITE
    
    print("Starting copy of local file %s to remote %s:%s" % (args.source, args.host, args.destination))
    now = datetime.now()
    
    try:
        with open(args.source, 'rb') as local_fh, sftp.open(args.destination, flags, mode) as remote_fh:
            for data in local_fh:
                remote_fh.write(data)
    except Exception as e:
        print("Error at sftpRead: ", str(e))
    
    timer(now)

def main(args):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((args.host, args.port))
    session = Session()
    session.handshake(sock)
    session.userauth_password(args.user, 'admin')
    if args.protocol == 'SCP':
        scpTransfer(args, session)
    elif args.protocol == 'FTP':
        sftpSend(args, session)


main(args)