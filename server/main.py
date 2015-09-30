#!/usr/bin/python
# main.py
# Python script to co-ordinate the sensors and actions
# ------------------------------------------------------------------------

from time          import sleep
from sensors       import Sensors
from xml_handler   import XML_Object
from logger        import log_handler
from job_scheduler import Sched_Obj

#=========================================================================#
#-------------------------------- INIT -----------------------------------#
#=========================================================================#

xml = XML_Object ()


INSIDE_PIR_STREAM_DURATION  = xml.inside_pir_trigger_stream_duration ()
OUTSIDE_PIR_STREAM_DURATION = xml.outside_pir_trigger_stream_duration ()
DOOR_SWITCH_STREAM_DURATION = xml.door_switch_trigger_stream_duration ()

del xml

# Set log level to LOW
log = log_handler (True)
log.set_log_level (log.LOG_LEVEL_LOW)

scheduler_obj = Sched_Obj ()

#=========================================================================#
#------------------------------ INIT END ---------------------------------#
#=========================================================================#

#=========================================================================#
#---------------------- INTERRUPT SERVICE ROUTINES -----------------------#
#=========================================================================#


def inside_pir_triggered_callback_func (channel):
    scheduler_obj.update_inside_pir_interrupt_timestamp ()

    log.print_high ('inside_pir_triggered_callback triggered')
    scheduler_obj.schedule_start_streaming ()
    scheduler_obj.schedule_stop_streaming (INSIDE_PIR_STREAM_DURATION)

    log.print_high ('exiting inside_pir_triggered_callback')
    return

#-------------------------------------------------------------------------#


def outside_pir_triggered_callback_func(channel):

    # This function also schedules an instapush notification to be sent
    scheduler_obj.increment_outside_PIR_interrupt_count ()
    scheduler_obj.update_outside_pir_interrupt_timestamp ()

    log.print_high ('outside_pir_triggered_callback triggered')
    scheduler_obj.schedule_start_streaming ()
    scheduler_obj.schedule_stop_streaming (OUTSIDE_PIR_STREAM_DURATION)
    log.print_high ('exiting outside_pir_triggered_callback')
    return

#-------------------------------------------------------------------------#

def door_switch_triggered_callback_func(channel):

    scheduler_obj.update_door_switch_interrupt_timestamp ()
    scheduler_obj.check_if_door_opened_from_outside_and_send_notif ()

    log.print_high ('door_switch_triggered_callback triggered')
    scheduler_obj.schedule_start_streaming ()
    scheduler_obj.schedule_stop_streaming (DOOR_SWITCH_STREAM_DURATION)

    log.print_high ('exiting door_switch_triggered_callback_func')
    return
    
#=========================================================================#
#------------------------------ MAIN LOOP --------------------------------#
#=========================================================================#

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

#=========================================================================#
#--------------------------------- END -----------------------------------#
#=========================================================================#