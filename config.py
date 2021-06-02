import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

PASSWORD = os.environ.get("SECRET_KEY")
SERVER = '192.168.2.104'
USERNAME = os.getlogin()
PORT = os.environ.get("PORT")
SOURCE_DIR_LOCATION = ""
SERVER_DIR_TREE_LOCATION = os.environ.get("SERVER_DIR_TREE")