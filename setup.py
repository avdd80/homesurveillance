#!/usr/bin/env python
# setup.py

from os import system

# Create a copy of xml_handler in server
system ('sudo cp client/xml_handler.py server/.')

# Make all scripts executable
system ('sudo chmod +x client/scripts/*')

