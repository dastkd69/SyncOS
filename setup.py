#!/usr/bin/env python

from distutils.core import setup
import sys
import subprocess

#subprocesses
subprocess.check_call(['apt-get', 'install', '-y', 'libssl-dev'])
subprocess.check_call(['apt-get', 'install', '-y', 'openssh'])
subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])


setup(name='SeverSync',
      description='File Tree Sync with Server over LAN',
      author='Tridib Das',
      author_email='dastkd27@gmail.com',
     )