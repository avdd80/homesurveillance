#!/usr/bin/env python
# tcp_monitor.py
# Monitors the remote TCP port. If the TCP port is open,
# it sends a UDP message to display_stream_launcher to
# start listening to the stream
from socket      import *
from time        import sleep
from xml_handler import XML_Object
from subprocess  import Popen, PIPE
from logger      import log_handler

log = log_handler (True)
log.set_log_level (log.LOG_LEVEL_LOW)

xml = XML_Object ()

REMOTE_TCP_IP_ADDR = xml.get_cam_server_ip ()
REMOTE_TCP_IP_PORT = xml.get_cam_server_port ()

DISPLAY_STREAM_LAUNCHER_IP   = xml.get_display_stream_launcher_ip ()
DISPLAY_STREAM_LAUNCHER_PORT = xml.get_display_stream_launcher_port ()
DISPLAY_STREAM_LAUNCHER_ADDR = (DISPLAY_STREAM_LAUNCHER_IP, DISPLAY_STREAM_LAUNCHER_PORT)

del xml

udp_send_sock = socket(AF_INET, SOCK_DGRAM)
is_stream_running = False


# Monitor process
def monitor_tcp_port ():

    is_tcp_port_open = False

    # Listen to the remote TCP port.
    monitor_proc = Popen('/bin/nc -z  ' + REMOTE_TCP_IP_ADDR + ' ' + str(REMOTE_TCP_IP_PORT) +'; echo $?', shell=True, stdout=PIPE)
    (stdout, stderr) = monitor_proc.communicate()
    log.print_notes (stdout)

    # If the TCP port is open, send a UDP message locally to start listening to the stream
    if (int (stdout) == 0):
        log.print_high ('TCP Port opened')
        is_tcp_port_open = True

    # Return True if a stream is running
    return is_tcp_port_open


#+---------------------------------+-------------------+------------------------+---------------------------+
#| Ret value from monitor_tcp_port | is_stream_running | Meaning                | Action                    |
#+---------------------------------+-------------------+------------------------+---------------------------+
#| False                           | False             | No change              | Ignore                    |
#+---------------------------------+-------------------+------------------------+---------------------------+
#| False                           | True              | Stream just turned off | Stop listening to stream  |
#+---------------------------------+-------------------+------------------------+---------------------------+
#| True                            | False             | Stream just turned on  | Start listening to stream |
#+---------------------------------+-------------------+------------------------+---------------------------+
#| True                            | True              | No change              | Ignore                    |
#+---------------------------------+-------------------+------------------------+---------------------------+

while (True):
    port_status = monitor_tcp_port ()

    # Check for a change in status
    if (is_stream_running != port_status):
        if (port_status == True):
            udp_send_sock.sendto ('LISTEN_TO_STREAM', DISPLAY_STREAM_LAUNCHER_ADDR)
            log.print_high ('LISTEN_TO_STREAM message sent')
            is_stream_running = True
        else:
            udp_send_sock.sendto ('STOP_LISTENING_TO_STREAM', DISPLAY_STREAM_LAUNCHER_ADDR)
            log.print_high ('STOP_LISTENING_TO_STREAM message sent')
            is_stream_running = False
