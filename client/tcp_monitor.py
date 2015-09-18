#!/usr/bin/env python
from subprocess import Popen, PIPE
from logger import log_handler
from time import sleep
from  socket import *

log = log_handler (True)
log.set_log_level (log.LOG_LEVEL_LOW)

REMOTE_TCP_IP_ADDR = '192.168.1.18'
REMOTE_TCP_IP_PORT = '8080'

HOST = '127.0.0.1'
TX_PORT = 1234
TX_ADDR = (HOST, TX_PORT)
udp_send_sock = socket(AF_INET, SOCK_DGRAM)
is_stream_running = False


# Monitor process
def monitor_tcp_port ():

    is_tcp_port_open = False

    # Listen to the remote TCP port.
    monitor_proc = Popen('/bin/nc -z  ' + REMOTE_TCP_IP_ADDR + ' ' + REMOTE_TCP_IP_PORT +'; echo $?', shell=True, stdout=PIPE)
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

# Let the UDP client start first
sleep (5)

while (True):
    port_status = monitor_tcp_port ()

    # Check for a change in status
    if (is_stream_running != port_status):
        if (port_status == True):
            udp_send_sock.sendto ('LISTEN_TO_STREAM', TX_ADDR)
            log.print_high ('LISTEN_TO_STREAM message sent')
            is_stream_running = True
        else:
            udp_send_sock.sendto ('STOP_LISTENING_TO_STREAM', TX_ADDR)
            log.print_high ('STOP_LISTENING_TO_STREAM message sent')
            is_stream_running = False
