#!/usr/bin/env python
# display_stream_launcher.py
# When a message is received from tcp_monitor, display_stream_launcher
# acts on it:
#
# if the received message is LISTEN_TO_STREAM, it turns on the display
# and opens omxplayer that listens to the remote TCP port for streaming
# video.
# if the message is STOP_LISTENING_TO_STREAM, it kills all instances of
# omxplayer and turns off the display.

from socket      import *
from time        import sleep
from xml_handler import XML_Object
from subprocess  import Popen, PIPE
from logger      import log_handler

log = log_handler (True)
log.set_log_level (log.LOG_LEVEL_LOW)

xml = XML_Object ()

DISPLAY_STREAM_LAUNCHER_ADDR = xml.get_display_stream_launcher_ip ()
DISPLAY_STREAM_LAUNCHER_PORT = xml.get_display_stream_launcher_port ()

REMOTE_TCP_IP_ADDR = xml.get_instapush_notif_ip ()
REMOTE_TCP_IP_PORT = xml.get_instapush_notif_port ()

log = log_handler (True)
log.set_log_level (log.LOG_LEVEL_LOW)

BUFSIZE = 128
RX_ADDR = (DISPLAY_STREAM_LAUNCHER_ADDR, DISPLAY_STREAM_LAUNCHER_PORT)
udp_recv_client = socket( AF_INET,SOCK_DGRAM)
udp_recv_client.setsockopt (SOL_SOCKET, SO_REUSEADDR, 1)
udp_recv_client.bind (RX_ADDR)
is_stream_active = False

Popen ('tcp_monitor.py', shell=True, stdout=PIPE)

while True:
    data = udp_recv_client.recv(BUFSIZE)
    
    # This message is received locally when the remote TCP port starts
    # streaming video
    if (data == 'LISTEN_TO_STREAM' or is_stream_active):
        Popen ('/opt/vc/bin/tvservice -p', shell=True, stdout=PIPE)
        display_stream_proc = Popen('/usr/bin/omxplayer --live --fps 10 ' + REMOTE_TCP_IP_ADDR + ':' + REMOTE_TCP_IP_PORT +'/?action=stream', shell=True, stdout=PIPE)
        #log.print_high('Poll = ' + display_stream_proc.poll())

    # This message is received locally when the remote TCP port is closed
    elif (data == 'STOP_LISTENING_TO_STREAM'):
        #log.print_high('Just before kill, Poll = ' + display_stream_proc.poll())
        Popen('pgrep omxplayer.bin | xargs kill', shell=True, stdout=PIPE)
        Popen ('/opt/vc/bin/tvservice -o', shell=True, stdout=PIPE)
        is_stream_active = False

    sleep (0.5)
