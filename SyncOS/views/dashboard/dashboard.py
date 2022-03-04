import sys
if '../../../' not in sys.path:
    sys.path.append('../../../')

import os
from bottle import route, run, template, static_file, request
import config

# modules
import src.modules.sysinfo as sysinfo


root = "./"
static_dir = root+"static/"
assets_dir = static_dir+"assets/"


@route('/')
@route('/dashboard')
@route('/home')
def dashboard():
    return template(root+"dashboard.html", sysinfo  = sysinfo.getInfo(config.SERVER_DIR_TREE_LOCATION))


@route('<filename:re:.*\.(jpg|png|svg)>')
def send_image(filename):
    return static_file(filename, root=root)

@route('/<filename:re:.*\.css>')
def static_dir(filename):
    return static_file(filename, root=root)

@route('/upload', method='POST')
def upload():
    uploads = request.files.getall('upload')
    # print(upload)
    save_path = config.SERVER_DIR_TREE_LOCATION

    for upload in uploads:
        file_path = f"{save_path}/{upload.raw_filename}"
        print(file_path)
        try:
            os.makedirs(file_path)
        except FileExistsError:
            upload.save(file_path)


#