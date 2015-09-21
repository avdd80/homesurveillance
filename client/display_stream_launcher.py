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
from commands    import getoutput
from xml_handler import XML_Object
from subprocess  import Popen, PIPE
from logger      import log_handler


log = log_handler (True)
log.set_log_level (log.LOG_LEVEL_LOW)

xml = XML_Object ()

DISPLAY_STREAM_LAUNCHER_ADDR = xml.get_display_stream_launcher_ip ()
DISPLAY_STREAM_LAUNCHER_PORT = xml.get_display_stream_launcher_port ()

REMOTE_TCP_IP_ADDR = xml.get_cam_server_ip ()
REMOTE_TCP_IP_PORT = xml.get_cam_server_port ()

# This number is different for every client
MY_CLIENT_NUMBER = 0
DISPLAY_TYPE = xml.get_client_display_type (MY_CLIENT_NUMBER)

del xml

log = log_handler (True)
log.set_log_level (log.LOG_LEVEL_LOW)

BUFSIZE = 128
RX_ADDR = (DISPLAY_STREAM_LAUNCHER_ADDR, DISPLAY_STREAM_LAUNCHER_PORT)
udp_recv_client = socket( AF_INET,SOCK_DGRAM)
udp_recv_client.setsockopt (SOL_SOCKET, SO_REUSEADDR, 1)
udp_recv_client.bind (RX_ADDR)


def is_process_running (process_name):
    process_list = getoutput('ps -A')
    if (process_name in process_list):
        return True
    else:
        return False

is_stream_active = False

# Kill any spurious instances of omxplayer
Popen ('sudo pkill omxplayer'    , shell=True, stdout=PIPE)
Popen ('sudo pkill omxplayer.bin', shell=True, stdout=PIPE)
omxplayer_running = False

#Popen ('/home/pi/homesurveillance/client/tcp_monitor.py', shell=True, stdout=PIPE)

while True:
    data = udp_recv_client.recv(BUFSIZE)
    
    # This message is received locally when the remote TCP port starts
    # streaming video
    if (data == 'LISTEN_TO_STREAM' or is_stream_active):
        if (DISPLAY_TYPE == 'HDMI'):
            Popen ('/opt/vc/bin/tvservice -p', shell=True, stdout=PIPE)
        
        # Start omxplayer only if it is not already running to avoid opening multiple
        # instances
        if (not omxplayer_running):
            display_stream_proc = Popen('/usr/bin/omxplayer --live --no-keys --fps 10 http://' + REMOTE_TCP_IP_ADDR + ':' + str (REMOTE_TCP_IP_PORT) +'/?action=stream', shell=True, stdout=PIPE)
            sleep (1)
        if ( (is_process_running ('omxplayer.bin')) or (is_process_running ('omxplayer')) ):
            omxplayer_running = True

    # This message is received locally when the remote TCP port is closed
    elif (data == 'STOP_LISTENING_TO_STREAM'):
        #log.print_high('Just before kill, Poll = ' + display_stream_proc.poll())
        if ( (is_process_running ('omxplayer.bin')) or (is_process_running ('omxplayer')) ):
            omxplayer_running = True
            Popen ('sudo pkill omxplayer'    , shell=True, stdout=PIPE)
            Popen ('sudo pkill omxplayer.bin', shell=True, stdout=PIPE)
        if (DISPLAY_TYPE == 'HDMI'):
            Popen ('/opt/vc/bin/tvservice -o', shell=True, stdout=PIPE)
        
        is_stream_active = False
        if ( (is_process_running ('omxplayer.bin') == False) and (is_process_running ('omxplayer') == False) ):
            omxplayer_running = False

    sleep (0.5)
