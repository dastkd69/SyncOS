import client

from android import AndroidService
from android.storage import app_storage_path
from android.storage import primary_external_storage_path
from android.storage import secondary_external_storage_path
from android.permissions import request_permissions, Permission


class ServiceExample(App):

    def start_service(self):
        self.service = AndroidService('Sevice example', 'service is running')
        self.service.start('Hello From Service')

    def stop_service(self):
        self.service.stop()

def runInBg

#request android permissions
request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])

#set hardcoded directory paths
settings_path = app_storage_path()
primary_ext_storage = primary_external_storage_path()
secondary_ext_storage = secondary_external_storage_path()

client.SOURCE_DIR_LOCATION = primary_ext_storage

#use in kivy different app 
#file chooser
# fileChooser = plyer.facades.FileChooser()
# dir_list = fileChooser.choose_dir(path=primary_ext_storage, multiple=True, title="Syncable Folders", on_selection=handle_selection)

def syncAllFolders():
    try:
        print("Trying SCP Transfer")
        client.initialise('SCP')
    except Exception as e:
        print("Failed SCP: ", str(e))
    else:
        print("Trying SFTP Transfer")
        client.initialise('FTP')
    finally:
        print("Failed Transfer! ")


def DirTreeWalker(source):
    filepaths = []
    for dirpath, dirnames, filenames in os.walk(source):
        filepaths.append = os.path.join(dirpath[len(source):], filenames)
        filepaths.append = os.path.join(dirpath[len(source):], )
        if not os.path.isdir(structure):
            os.mkdir(structure)
        else:
            print("Folder does already exits!")

