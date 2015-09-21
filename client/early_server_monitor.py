#!/usr/bin/env python
# early_server_monitor.py
# Monitors a remote UDP port for message to indicate that the
# server has started streaming. The UDP message is forwarded 
# to display_stream_launcher to start listening to the video 
# stream
# If this monitor fails to receive the message, the tcp_monitor
# can start the stream display
from socket      import *
from time        import sleep
from xml_handler import XML_Object
from subprocess  import Popen, PIPE
from logger      import log_handler

log = log_handler (True)
log.set_log_level (log.LOG_LEVEL_LOW)

# This number is different for every client
MY_CLIENT_NUMBER = 0

BUFSIZE = 128
xml = XML_Object ()
MY_IP   = xml.get_client_ip   (MY_CLIENT_NUMBER)
MY_PORT = xml.get_client_port (MY_CLIENT_NUMBER)
MY_LISTENING_ADDR = (MY_IP, MY_PORT)
del xml

DISPLAY_STREAM_LAUNCHER_IP   = xml.get_display_stream_launcher_ip ()
DISPLAY_STREAM_LAUNCHER_PORT = xml.get_display_stream_launcher_port ()
DISPLAY_STREAM_LAUNCHER_ADDR = (DISPLAY_STREAM_LAUNCHER_IP, DISPLAY_STREAM_LAUNCHER_PORT)

while True:
    # Blocking call
    data = udp_recv_client.recv(BUFSIZE)
    
    # This message is received from the remote server when
    # video streaming starts
    if (data == 'LISTEN_TO_STREAM'):
        udp_send_sock.sendto ('LISTEN_TO_STREAM', DISPLAY_STREAM_LAUNCHER_ADDR)
        log.print_high ('early_server_monitor: Sent LISTEN_TO_STREAM')

    # Sleep for 5 seconds to avoid receiving multiple UDP messages
    # The UDP server DOES send multiple UDP messages
    sleep (5)
