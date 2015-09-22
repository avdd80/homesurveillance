#!/usr/bin/python
# main.py
# Python script to co-ordinate the sensors and actions
# ------------------------------------------------------------------------

from socket      import *
from time        import sleep
from sensors     import Sensors
from xml_handler import XML_Object
from logger      import log_handler
from pitftscreen import PiTFT_Screen
from cam_server  import Cam_Object

xml = XML_Object ()

INSTAPUSH_NOTIF_HOST = xml.get_instapush_notif_ip ()
INSTAPUSH_NOTIF_PORT = xml.get_instapush_notif_port ()
INSTAPUSH_NOTIF_ADDR = (INSTAPUSH_NOTIF_HOST, INSTAPUSH_NOTIF_PORT)
udp_send_sock        = socket(AF_INET, SOCK_DGRAM)

del xml

# Set log level to LOW
log = log_handler (True)
log.set_log_level (log.LOG_LEVEL_LOW)

# Create TFT display object
pitft = PiTFT_Screen ()
log.print_high ('Created TFT display object')

cam   = Cam_Object ()
log.print_high ('Created camera object')

# Create sensors object
sensors_obj = Sensors (inside_pir_triggered_callback_func, outside_pir_triggered_callback_func,
                       door_switch_triggered_callback_func)
log.print_high ('Created sensors object')

def inside_pir_triggered_callback_func (channel):
    sensors_obj.disable_InsidePIRInterrupt ()
    log.print_high ('inside_pir_triggered_callback triggered')
    udp_send_sock.sendto ('You are in front of the door', INSTAPUSH_NOTIF_ADDR)
    log.print_high ('Starting camera')
    if (cam.start_camera ('320x240', '5', 'night')):
        pitft.Backlight (True)
        log.print_high ('main: Starting stream_video_to_display...')
        pitft.stream_video_to_display ()
    else:
        log.print_high ('main: Camera already on')
    log.print_high ('Sleeping for 120 s')
    
    # TODO: implement as a retriggered scheduler
    sleep (120)
    log.print_high ('Done sleeping for 120 s. Stopping stream...')
    pitft.stop_stream_video_to_display ()
    log.print_high ('Stream stoppped. Turning backlight off...')
    pitft.Backlight (False)
    log.print_high ('Backlight off. Stopping camera...')
    if (cam.stop_camera ()):
        log.print_high ('main: Camera off')
    else:
        log.print_high ('main: Could not turn off camera')
    log.print_high ('exiting inside_pir_triggered_callback')
    sensors_obj.enable_InsidePIRInterrupt (inside_pir_triggered_callback_func)

def outside_pir_triggered_callback_func(channel):
    sensors_obj.disable_OutsidePIRInterrupt ()
    log.print_high ('outside_pir_triggered_callback triggered')
    sensors_obj.enable_OutsidePIRInterrupt (outside_pir_triggered_callback_func)

    
def door_switch_triggered_callback_func(channel):
    sensors_obj.disable_DoorSwitchInterrupt ()
    log.print_high ('door_switch_triggered_callback triggered')
    udp_send_sock.sendto ('Door opened', INSTAPUSH_NOTIF_ADDR)
    cam.start_camera ('320x240', '5', 'night')
    pitft.Backlight (True)
    pitft.stream_video_to_display ()

    # TODO: implement as a retriggered scheduler
    sleep (120)
    pitft.stop_stream_video_to_display ()
    pitft.Backlight (False)
    cam.stop_camera ()
    log.print_high ('exiting door_switch_triggered_callback triggered')
    sensors_obj.enable_DoorSwitchInterrupt (door_switch_triggered_callback_func)
    

def main ():
    log.print_high ('Starting...')
    log.print_high ('Started logger object')

    # Start Framebuffer copy daemon
    pitft.start_fbcp_process()

    i = 0
    while (True):
        if (i == 10):
            i = 0
            log.print_high ('Waiting...')
        else:
            i = i + 1
        sleep (1)

if __name__ == "__main__":
    main ()

# Create motion service handler (stopped by default)
#motion_service = motion ()
#log.print_high ('Created motion service handler')


