#!/usr/bin/env python
# job_scheduler.py
# Responsible for scheduling all the importants jobs
import sys
import logging
import time, datetime
from   socket      import *
from   xml_handler import XML_Object
from   logger      import log_handler
from   pitftscreen import PiTFT_Screen
from   cam_server  import Cam_Object
# APScheduler > 3.0.0
from   apscheduler.schedulers.background import BackgroundScheduler
# APScheduler == 2.1.2
#from apscheduler.scheduler import Scheduler

log = log_handler (True)
log.set_log_level (log.LOG_LEVEL_LOW)

# For APScheduler > 3.0.0
logging.basicConfig()


def get_elapsed_seconds_since (timestamp):
    current_time = datetime.datetime.now ()
    return int ((current_time - timestamp).total_seconds())
    

class Sched_Obj:

#=========================================================================#
#-------------------------------- INIT -----------------------------------#
#=========================================================================#

    def __init__(self):
        
        self.__xml = XML_Object ()
#        self.__JOB_SCHED_IP         = self.__xml.get_job_scheduler_ip ()
#        self.__JOB_SCHED_PORT       = self.__xml.get_job_scheduler_port ()
#        self.__JOB_SCHED_RECV_ADDR  = (self.__JOB_SCHED_IP, self.__JOB_SCHED_PORT)

#-------------------------------------------------------------------------#
#----------------------------- SCHEDULER INIT ----------------------------#
#-------------------------------------------------------------------------#

        self.__sched = BackgroundScheduler()
        self.__sched.start()        # start the scheduler
        log.print_high ('Scheduler started')
#-------------------------------------------------------------------------#
#----------------------------- INSTAPUSH INIT ----------------------------#
#-------------------------------------------------------------------------#

        self.__INSTAPUSH_NOTIF_IP   = self.__xml.get_instapush_notif_ip ()
        self.__INSTAPUSH_NOTIF_PORT = self.__xml.get_instapush_notif_port ()
        self.__INSTAPUSH_NOTIF_ADDR = (self.__INSTAPUSH_NOTIF_IP, self.__INSTAPUSH_NOTIF_PORT)

        udp_send_sock.sendto ('Test message from init', self.__INSTAPUSH_NOTIF_ADDR)

        self.__min_gap_between_two_instapush_notif = self.__xml.min_gap_between_two_instapush_notif ()
        # Record the timestamp when the last instapush notification was sent
        self.__last_instapush_notif_sent_at = datetime.datetime.now ()
        
        self.__is_stream_job_running        = False
        self.__outside_PIR_interrupt_count  = 0
        
        self.__instapush_notif_timeout_job  = self.__sched.add_job(self.send_instapush_notif, 'interval', seconds = 5, args=['Dummy message'])
        self.__instapush_notif_timeout_job.remove ()

#-------------------------------------------------------------------------#
#--------------------------- PITFT SCREEN INIT ---------------------------#
#-------------------------------------------------------------------------#

        # Create TFT display object
        self.__pitft = PiTFT_Screen ()
        log.print_high ('Created TFT display object')

        # Start Framebuffer copy daemon
        self.__pitft.start_fbcp_process()

        self.__cam   = Cam_Object ()
        log.print_high ('Created camera object')

        # Create a dummy job and cancel it
        
        self.__stream_job = self.__sched.add_job(self.stop_streaming_cb, 'interval', seconds = 5)
        self.__stream_job.remove ()

        log.print_high ('Scheduler init done')
        
#-------------------------------------------------------------------------#
#---------------------------- INTERRUPTS INIT ----------------------------#
#-------------------------------------------------------------------------#

        self.__last_inside_pir_interrupt_triggered_at  = datetime.datetime.now ()
        self.__last_outside_pir_interrupt_triggered_at = datetime.datetime.now ()
        self.__last_door_switch_interrupt_triggered_at = datetime.datetime.now ()
        

#=========================================================================#
#------------------------------ INIT END ---------------------------------#
#=========================================================================#


#-------------------------------------------------------------------------#
#-------------------- INTERRUPT TRIGGERED FUNCTIONS  ---------------------#
#-------------------------------------------------------------------------#

    def update_inside_pir_interrupt_timestamp (self):
        self.__last_inside_pir_interrupt_triggered_at  = datetime.datetime.now ()
        
    def how_long_ago_was_last_inside_pir_interrupt_triggered (self):
        return get_elapsed_seconds_since (self.__last_inside_pir_interrupt_triggered_at)
        
#-------------------------------------------------------------------------#
        
    def update_outside_pir_interrupt_timestamp (self):
        self.__last_outside_pir_interrupt_triggered_at = datetime.datetime.now ()
        
    def how_long_ago_was_last_inside_pir_interrupt_triggered (self):
        return get_elapsed_seconds_since (self.__last_outside_pir_interrupt_triggered_at)

#-------------------------------------------------------------------------#
        
    def update_door_switch_interrupt_timestamp (self):
        self.__last_door_switch_interrupt_triggered_at = datetime.datetime.now ()
        
    def how_long_ago_was_last_inside_pir_interrupt_triggered (self):
        return get_elapsed_seconds_since (self.__last_door_switch_interrupt_triggered_at)

#-------------------------------------------------------------------------#
#---------------------- INSTAPUSH NOTIFICATION HANDLER -------------------#
#-------------------------------------------------------------------------#

    def how_long_ago_was_last_instapush_notif_sent (self):
        return get_elapsed_seconds_since (self.__last_instapush_notif_sent_at)

#-------------------------------------------------------------------------#
    # Send an instapush notification if we get more than 
    # 2 interrupts (reconfigurable) during the timout (also reconfigurable)
    # To avoid flooding notifications, allow a minimum gap between two 
    # notifications. Currently set to 5 minutes (reconfigurable)
    
    def send_instapush_notif (self, notif_message):
        # Remove the interval job
        self.__instapush_notif_timeout_job.remove ()
        
        log.print_high ('send_instapush_notif triggered')
        
        # Check the interrupt count during the timeout. If greater than the
        # threshold, send a notification.
        # Also check when the last notification was sent. 
        if ( (self.__outside_PIR_interrupt_count > self.__xml.get_instapush_notif_interrupt_count()) and 
             (self.how_long_ago_was_last_instapush_notif_sent () > self.__min_gap_between_two_instapush_notif) ):
            log.print_high ('Will send a notif now')
            udp_send_sock.sendto (notif_message, self.__INSTAPUSH_NOTIF_ADDR)
            self.__last_instapush_notif_sent_at = datetime.datetime.now ()
        else:
            log.print_high ('No notif. Last notif sent ' + str (self.how_long_ago_was_last_instapush_notif_sent ()) 
                             + 's ago. Interrupt count = ' + str (self.__outside_PIR_interrupt_count))
            
        # Reset the counter for the current cycle
        self.__outside_PIR_interrupt_count = 0
        return
#-------------------------------------------------------------------------#
    # Count the number of interrupts in 20 seconds (reconfigurable) to ensure a
    # person is standing outside the door
    def schedule_instapush_notif_timeout (self, instapush_notif_timeout = 20):
        instapush_notif_timeout = self.__xml.get_instapush_notif_timeout ()
        self.__instapush_notif_timeout_job = self.__sched.add_job(self.send_instapush_notif, 'interval', 
                                                  seconds=instapush_notif_timeout, args=['Someone at the door'])
        log.print_high ('Scheduled instapush_notif_timeout for ' + str (instapush_notif_timeout) + 's')
        return

#-------------------------------------------------------------------------#
        
    def check_if_door_opened_from_outside_and_send_notif (self):
        # Check if someone was recently inside the house, behind the door
        if (self.how_long_ago_was_last_inside_pir_interrupt_triggered () > xml.inside_home_presence_timeout()):
            # If no one was inside the house and door was opened, send a notification
            self.send_instapush_notif ('Door opened')
        

#-------------------------------------------------------------------------#

    # Increment interrupt count and start a timer
    def increment_outside_PIR_interrupt_count (self):
        if (self.__outside_PIR_interrupt_count == 0):
            self.schedule_instapush_notif_timeout ()
        self.__outside_PIR_interrupt_count = self.__outside_PIR_interrupt_count + 1
        log.print_high ('# of interrupts = ' + str (self.__outside_PIR_interrupt_count))
        return

#-------------------------------------------------------------------------#
#------------------------------ STREAM HANDLER ---------------------------#
#-------------------------------------------------------------------------#

    # Implemented as a callback function
    def start_streaming_cb (self):
        if (not self.__is_stream_job_running):
            log.print_high ('Starting camera...')
            if (self.__cam.start_camera ('320x240', '5', 'night')):
                self.__pitft.Backlight (True)
                log.print_high ('scheduler: Starting stream_video_to_display...')
                self.__pitft.stream_video_to_display ()
            else:
                log.print_high ('scheduler: Camera already on')
            self.__is_stream_job_running = True
        return
#-------------------------------------------------------------------------#
    # Turns off camera streaming. 
    # Turns off local display
    def stop_streaming_cb (self):

        # First cancel the interval job
        self.__stream_job.remove ()
        log.print_high ('Stopping stream...')
        self.__pitft.stop_stream_video_to_display ()
        log.print_high ('Stream stoppped. Turning backlight off...')
        self.__pitft.Backlight (False)
        log.print_high ('Backlight off. Stopping camera...')
        
        if (self.__cam.stop_camera ()):
            log.print_high ('scheduler: Camera off')
            self.__is_stream_job_running = False
        else:
            log.print_high ('scheduler: Could not turn off camera')
        log.print_high ('exiting inside_pir_triggered_callback')
        return
#-------------------------------------------------------------------------#
    # Default schedule delay is 0 minutes
    def schedule_start_streaming (self, delay = 0):
        if (delay == 0):
            self.start_streaming_cb ()
        return
#-------------------------------------------------------------------------#
    # Default schedule delay is 4 minutes
    def schedule_stop_streaming (self, seconds_delay = 240):
        
        # Blindly cancel the job before scheduling it
        self.__stream_job.remove ()
        self.__stream_job = self.__sched.add_job(self.stop_streaming_cb, 'interval', seconds = seconds_delay)
        #self.__stream_job = self.__sched.add_date_job(self.stop_streaming_cb, datetime.datetime.today () + datetime.timedelta (seconds = seconds_delay))
        log.print_high ('Will turn off stream after ' + str (seconds_delay) + 's from now')
        return
#=========================================================================#
#--------------------------------- END -----------------------------------#
#=========================================================================#
