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

def initialise():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER, int(PORT)))
    session = Session()
    session.handshake(sock)
    session.userauth_password(USERNAME, PASSWORD)
    sftp = session.sftp_init()
    return sftp
