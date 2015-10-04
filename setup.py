#!/usr/bin/env python
# setup.py

from os         import system, getcwd
from subprocess import Popen, PIPE

working_dir = getcwd ()

# Make all scripts executable
system ('sudo chmod +x ' + working_dir + '/scripts/*')

# Make all python scripts executable
# Server
system ('sudo chmod +x ' + working_dir + '/server/instapush_notif.py')
system ('sudo chmod +x ' + working_dir + '/server/main.py')

# Client
system ('sudo chmod +x ' + working_dir + '/client/display_stream_launcher.py')
system ('sudo chmod +x ' + working_dir + '/client/tcp_monitor.py')
system ('sudo chmod +x ' + working_dir + '/client/early_server_monitor.py')

# Create startup script
system ('sudo ln -s '    + working_dir + '/scripts/server_batch_launcher.sh /etc/init.d/server_batch_launcher.sh')

# Set the correct timezone
system ('sudo ln -sf /usr/share/zoneinfo/America/Los_Angeles /etc/localtime')

# Start client processes
#Popen ('client/display_stream_launcher.py' , shell=True, stdout=PIPE)

# Start server processes
#Popen ('server/instapush_notif.py'    , shell=True, stdout=PIPE)
#Popen ('server/main.py'               , shell=True, stdout=PIPE)
