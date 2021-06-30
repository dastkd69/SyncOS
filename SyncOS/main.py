from views.dashboard import dashboard
import config
import os
from bottle import route, run, template, static_file, request, mount

root = "blueprint/views/"
dashboard_root = root+"dashboard/"
static_dir = dashboard_root+"static/"
assets_dir = static_dir+"assets/"

mount('/', dashboard)

if __name__ == '__main__':
    run(host='0.0.0.0', port=config.MAIN_PORT, server='bjoern', reloader=True, debug=True)