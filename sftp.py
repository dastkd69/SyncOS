from __future__ import print_function

import os

from ssh2.session import Session
from ssh2.sftp import LIBSSH2_FXF_READ, LIBSSH2_FXF_CREAT, LIBSSH2_FXF_WRITE, LIBSSH2_SFTP_S_IRUSR, LIBSSH2_SFTP_S_IRGRP, LIBSSH2_SFTP_S_IWUSR, LIBSSH2_SFTP_S_IROTH


source = '/home/yuri/Downloads/'
destination = '/home/yuri/Temporary/'

# def mv(structure, filenames):
#     while True:
#         try:
#             #sftp_send((filename for filename  in filenames), structure)
#             for filename in filenames:
#                 subprocess.call(f'cp -r {structure+filename} {structure+filename}', shell=True)
#         except Exception as e:
#             print(str(e))

def sftpGet(sftp, session, source, destination):    
    try:
        with sftp.open(source, LIBSSH2_FXF_READ, LIBSSH2_SFTP_S_IRUSR) as remote_fh, open(destination, 'wb') as local_fh:
            for _, data in remote_fh:
                local_fh.write(data)
    except Exception as e:
        print("Error at sftpRead: ", str(e))

def sftpSend(sftp, source, destination):
    mode = LIBSSH2_SFTP_S_IRUSR | LIBSSH2_SFTP_S_IWUSR | LIBSSH2_SFTP_S_IRGRP | LIBSSH2_SFTP_S_IROTH
    flags = LIBSSH2_FXF_CREAT | LIBSSH2_FXF_WRITE
    
    print(f"Starting copy of local file {source} to remote server:{destination}")
    
    try:
        with open(source, 'rb') as local_fh, sftp.open(destination, flags, mode) as remote_fh:
            for data in local_fh:
                remote_fh.write(data)
    except Exception as e:
        print("Error at sftpRead: ", str(e))
    
def syncDirectoryTree(sftp):
    folderstat = os.stat(source).st_mode & 0o777
    filepaths, destination_filepaths = [], []
    for dirpath, _, filenames in os.walk(source):
        full_dir_path_Destination = os.path.join(destination, dirpath[len(source):])
        #if not os.path.isdir(structure):
        try:
            sftp.mkdir(full_dir_path_Destination, folderstat)
            #os.mkdir(full_dir_path_Destination)
        except Exception as e:
            print(str(e))
        for filename in filenames:
            filepaths.append(os.path.join(dirpath, filename))
            destination_filepaths.append(os.path.join(full_dir_path_Destination, filename))
    return filepaths, destination_filepaths

def initialise(session):
    sftp = session.sftp_init()
    filepaths, destination_filepaths = syncDirectoryTree(sftp)
    map(sftpGet, filepaths, destination_filepaths)
    




