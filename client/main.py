#!/usr/bin/python
# main.py
# Python script to co-ordinate the sensors and actions
# ------------------------------------------------------------------------

from socket      import *
from time        import sleep
from os          import system
from sensors     import Sensors
from xml_handler import XML_Object
from logger      import log_handler
from pitftscreen import PiTFT_Screen

xml = XML_Object ()

INSTAPUSH_NOTIF_HOST = xml.get_instapush_notif_ip ()
INSTAPUSH_NOTIF_PORT = xml.get_instapush_notif_port ()
INSTAPUSH_NOTIF_ADDR = (INSTAPUSH_NOTIF_HOST, INSTAPUSH_NOTIF_PORT)
udp_send_sock        = socket(AF_INET, SOCK_DGRAM)

# Set log level to LOW
log = log_handler (True)
log.set_log_level (log.LOG_LEVEL_LOW)


def inside_pir_triggered_callback_func (channel):
    log.print_high ('inside_pir_triggered_callback triggered')
    udp_send_sock.sendto ('You are in front of the door', INSTAPUSH_NOTIF_ADDR)
    pitft.Backlight (True)
    pitft.stream_video_to_display ()
    sleep (10)
    pitft.stop_stream_video_to_display ()
    pitft.Backlight (False)
    log.print_high ('exiting inside_pir_triggered_callback')

def outside_pir_triggered_callback_func(channel):
    log.print_high ('outside_pir_triggered_callback triggered')
    
def door_switch_triggered_callback_func(channel):
    log.print_high ('door_switch_triggered_callback triggered')
    

if __name__ == "__main__":
    def main ():
        log.print_high ('Starting...')
        log.print_high ('Started logger object')

        # Start Framebuffer copy daemon
        system ('/usr/bin/fbcp &')

        # Create TFT display object
        pitft = PiTFT_Screen ()
        log.print_low ('Created TFT display object')

        # Create sensors object
        sensors_obj = Sensors (inside_pir_triggered_callback_func, outside_pir_triggered_callback_func,
                          door_switch_triggered_callback_func)
        log.print_low ('Created sensors object')
        i = 0
        while (True):
            if (i == 20):
                i = 0
                log.print_low ('Waiting...')
            else:
                i = i + 1
            sleep (0.1)

# Create motion service handler (stopped by default)
#motion_service = motion ()
#log.print_low ('Created motion service handler')


