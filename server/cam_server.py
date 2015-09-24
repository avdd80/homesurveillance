#!/usr/bin/env python
# cam_server_launcher.py
from socket      import *
from time        import sleep
from commands    import getoutput
from xml_handler import XML_Object
from subprocess  import Popen, PIPE
from logger      import log_handler

log = log_handler (True)
log.set_log_level (log.LOG_LEVEL_LOW)

udp_send_sock        = socket(AF_INET, SOCK_DGRAM)

def is_process_running (process_name):
    process_list = getoutput('ps -A')
    if (process_name in process_list):
        return True
    else:
        return False

class Cam_Object:

    def __init__(self):
    
        xml = XML_Object ()
        self.__is_cam_started = False
        self.__mjpeg_streamer_root_path = xml.get_mjpg_streamer_path ()
        self.__mjpg_streamer_path       = xml.get_mjpg_streamer_path ()
        # Returns numerical port number
        self.__CAM_SERVER_PORT          = str (xml.get_cam_server_port ())
        
        Popen ('export LD_LIBRARY_PATH=' + self.__mjpeg_streamer_root_path, shell=True, stdout=PIPE)
        del xml
    
    # This function sets the current cam status 
    def set_cam_status (self, new_cam_status):
        self.__is_cam_started = new_cam_status
        
    def get_cam_status (self):
        if (is_process_running ('mjpg_streamer')):
            log.print_high ('mjpg_streamer running')
            self.set_cam_status (True)
        else:
            log.print_high ('mjpg_streamer not running')
            self.set_cam_status (False)
        return self.__is_cam_started

    # This function sends 10 back to back messages to the client(s)
    # to allow them to start listening to the streams asap to reduce
    # the client side delay
    def early_message_to_client (self):
        xml = XML_Object ()
        
        CLIENT_COUNT = xml.get_client_count ()
        i = 0
        while (i < CLIENT_COUNT):
            CLIENT_LISTNER_UDP_IP   = xml.get_client_ip   (i)
            CLIENT_LISTNER_UDP_PORT = xml.get_client_port (i)
            CLIENT_ADDR = (CLIENT_LISTNER_UDP_IP, CLIENT_LISTNER_UDP_PORT)
            udp_send_sock.sendto ('LISTEN_TO_STREAM', CLIENT_ADDR)
        del xml

    def start_camera(self, resolution='320x240', fps='5', exposure_mode=''):

        # Start camera only if it is not already started
        if (not self.get_cam_status ()):

            Popen ('sudo fbi -T 2 -d /dev/fb0 -noverbose -a ../images/rpi_cam_splash_320x240.png', shell=True, stdout=PIPE)
            log.print_high ('cam_server: Starting camera...')

            # Available scripts
            # start_cam_320x240_10.sh        start_cam_640x480_10.sh
	    # start_cam_320x240_10_night.sh  start_cam_640x480_10_night.sh
	    # start_cam_320x240_2.sh         start_cam_640x480_2.sh
	    # start_cam_320x240_2_night.sh   start_cam_640x480_2_night.sh
	    # start_cam_320x240_5.sh         start_cam_640x480_5.sh
	    # start_cam_320x240_5_night.sh   start_cam_640x480_5_night.sh
        

            start_cam_script = '../scripts/start_cam_'
            start_cam_script = start_cam_script + resolution + '_'
            start_cam_script = start_cam_script + fps + '_'
            if (exposure_mode != ''):
                start_cam_script = start_cam_script + exposure_mode
            start_cam_script = start_cam_script + '.sh'

            log.print_high ('Running camera script:\n' + start_cam_script)
            Popen(start_cam_script, shell=True, stdout=PIPE)
            sleep (2)

            timeout = 10
            while ( (self.get_cam_status () == False) and (timeout > 0) ):

                Popen(start_cam_script, shell=True, stdout=PIPE)
                timeout = timeout - 1
                log.print_high ('Starting camera. Number retries left: ' + str(timeout))
                sleep (2)
        else:
            log.print_high ('Multiple triggers received. Camera already running')

        return self.get_cam_status ()
              
            
    def stop_camera(self):
        timeout = 10
        log.print_high ('Killing camera...')
        Popen ('sudo pkill mjpg_streamer', shell=True, stdout=PIPE)
        sleep (2)
        while ((self.get_cam_status () == True) and timeout > 0):
            Popen ('sudo pkill mjpg_streamer', shell=True, stdout=PIPE)
            timeout = timeout - 1
            log.print_high ('Killing mjpg_streamer. Number retries left: ' + str(timeout))
            sleep (2)
        
        # get_cam_status returns the status of the camera. If True,
        # camera is ON. If False, camera is OFF. The flag must be inverted
        # for the calling function to interpret the return value
        # correctly: True == SUCCESS (cam off), False == FAILURE (Cam on)
        return (not self.get_cam_status ())
