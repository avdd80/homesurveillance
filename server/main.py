#!/usr/bin/python
# main.py
# Python script to co-ordinate the sensors and actions
# ------------------------------------------------------------------------

from socket        import *
from time          import sleep
from sensors       import Sensors
from xml_handler   import XML_Object
from logger        import log_handler
from job_scheduler import Sched_Obj
#from pitftscreen import PiTFT_Screen
#from cam_server  import Cam_Object


xml = XML_Object ()

INSTAPUSH_NOTIF_HOST = xml.get_instapush_notif_ip ()
INSTAPUSH_NOTIF_PORT = xml.get_instapush_notif_port ()
INSTAPUSH_NOTIF_ADDR = (INSTAPUSH_NOTIF_HOST, INSTAPUSH_NOTIF_PORT)
udp_send_sock        = socket(AF_INET, SOCK_DGRAM)

del xml

# Set log level to LOW
log = log_handler (True)
log.set_log_level (log.LOG_LEVEL_LOW)

scheduler_obj = Sched_Obj ()


is_interrupt_already_processing = False
def inside_pir_triggered_callback_func (channel):

    scheduler_obj.increment_outside_PIR_interrupt_count ()
    # Make the ISR (kind of) atomic by disallowing nested interrupts to process
    if (scheduler_obj.is_stream_running ()):
        log.print_high ('Nested inside_pir_triggered_callback triggered. Returning')
        return
    else:
        # CRITICAL SECTION
        log.print_high ('inside_pir_triggered_callback triggered')
        udp_send_sock.sendto ('You are in front of the door', INSTAPUSH_NOTIF_ADDR)
        scheduler_obj.schedule_start_streaming ()
        scheduler_obj.schedule_stop_streaming (10)
        log.print_high ('exiting inside_pir_triggered_callback')

def outside_pir_triggered_callback_func(channel):
    log.print_high ('outside_pir_triggered_callback triggered')

    
def door_switch_triggered_callback_func(channel):
    log.print_high ('door_switch_triggered_callback triggered')
    udp_send_sock.sendto ('Door opened', INSTAPUSH_NOTIF_ADDR)
    #cam.start_camera ('320x240', '5', 'night')
    #pitft.Backlight (True)
    #pitft.stream_video_to_display ()

    # TODO: implement as a retriggered scheduler
    sleep (120)
    #pitft.stop_stream_video_to_display ()
    #pitft.Backlight (False)
    #cam.stop_camera ()
    log.print_high ('exiting door_switch_triggered_callback triggered')
    

def main ():
    log.print_high ('Starting...')
    log.print_high ('Started logger object')
    
    # Create sensors object
    sensors_obj = Sensors (inside_pir_triggered_callback_func, outside_pir_triggered_callback_func,
                      door_switch_triggered_callback_func)

    log.print_high ('Created sensors object')

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


