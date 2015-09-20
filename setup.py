#!/usr/bin/env python
# setup.py

from os         import system
from subprocess import Popen, PIPE

# Make all scripts executable
system ('sudo chmod +x scripts/*')
system ('sudo chmod +x scripts/*')

# Make all python scripts executable
system ('sudo chmod +x server/instapush_notif.py')
system ('sudo chmod +x server/main.py')

system ('sudo chmod +x client/display_stream_launcher.py')
system ('sudo chmod +x client/tcp_monitor.py')

# Start client processes
#Popen ('client/display_stream_launcher.py' , shell=True, stdout=PIPE)

# Start server processes
#Popen ('server/instapush_notif.py'    , shell=True, stdout=PIPE)
#Popen ('server/main.py'               , shell=True, stdout=PIPE)
