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
system ('sudo chmod +x client/early_server_monitor.py')

# Make autostart scripts executable
system ('sudo chmod +x scripts/instapush_notif.desktop')
system ('sudo chmod +x scripts/main.desktop')

system ('sudo mkdir                              /home/pi/.config/autostart')
system ('sudo mv scripts/instapush_notif.desktop /home/pi/.config/autostart/.')
system ('sudo mv scripts/main.desktop            /home/pi/.config/autostart/.')


# Set the correct timezone
system ('sudo ln -sf /usr/share/zoneinfo/America/Los_Angeles /etc/localtime')

# Start client processes
#Popen ('client/display_stream_launcher.py' , shell=True, stdout=PIPE)

# Start server processes
#Popen ('server/instapush_notif.py'    , shell=True, stdout=PIPE)
#Popen ('server/main.py'               , shell=True, stdout=PIPE)
