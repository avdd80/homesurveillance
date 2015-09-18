#!/usr/bin/env python
# display_stream_launcher.py
from subprocess import Popen, PIPE
from logger import log_handler
from time import sleep
from  socket import *

log = log_handler (True)
log.set_log_level (log.LOG_LEVEL_LOW)

BUFSIZE = 128
HOST = '127.0.0.1'
RX_PORT = 1234
RX_ADDR = (HOST, RX_PORT)
udp_recv_client = socket( AF_INET,SOCK_DGRAM)
udp_recv_client.setsockopt (SOL_SOCKET, SO_REUSEADDR, 1)
udp_recv_client.bind (RX_ADDR)
is_stream_active = False


while True:
    data = udp_recv_client.recv(BUFSIZE)
    if (data == 'LISTEN_TO_STREAM' or is_stream_active):
        Popen ('/opt/vc/bin/tvservice -p', shell=True, stdout=PIPE)
        display_stream_proc = Popen('/usr/bin/omxplayer --live --fps 10 http://192.168.1.18:8080/?action=stream', shell=True, stdout=PIPE)
        #log.print_high('Poll = ' + display_stream_proc.poll())
    elif (data == 'STOP_LISTENING_TO_STREAM'):
        #log.print_high('Just before kill, Poll = ' + display_stream_proc.poll())
        Popen('pgrep omxplayer.bin | xargs kill', shell=True, stdout=PIPE)
        Popen ('/opt/vc/bin/tvservice -o', shell=True, stdout=PIPE)
        is_stream_active = False

    sleep (0.5)
