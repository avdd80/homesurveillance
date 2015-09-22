#!/usr/bin/env python
# job_scheduler.py
import sys
import logging
import time, datetime
from   socket      import *
from   xml_handler import XML_Object
from   logger      import log_handler
from   pitftscreen import PiTFT_Screen
from   cam_server  import Cam_Object
from   apscheduler.schedulers.blocking import BlockingScheduler

log = log_handler (True)
log.set_log_level (log.LOG_LEVEL_LOW)

logging.basicConfig()

class Sched_Obj:

    def __init__(self):
        
        xml = XML_Object ()
        self.__BUFSIZE             = 128
        self.__JOB_SCHED_IP        = xml.get_job_scheduler_ip ()
        self.__JOB_SCHED_PORT      = xml.get_job_scheduler_port ()
        self.__JOB_SCHED_RECV_ADDR = (self.__JOB_SCHED_IP, self.__JOB_SCHED_PORT)
        
        del xml

	# Create TFT display object
	self.__pitft = PiTFT_Screen ()
	log.print_high ('Created TFT display object')
	
	# Start Framebuffer copy daemon
        self.__pitft.start_fbcp_process()
	
	self.__cam   = Cam_Object ()
        log.print_high ('Created camera object')

        log.print_high ('Before Blocking scheduler obj')
        self.__sched = BlockingScheduler()
        log.print_high ('Blocking scheduler obj created')
        self.__sched.start()        # start the scheduler
        log.print_high ('Scheduler started')

        # Create a dummy job and cancel it
        self.__stream_job = self.__sched.add_job(stop_streaming_cb, datetime.datetime.today () + datetime.timedelta (seconds = 5))
        self.__stream_job.cancel_job ()

        log.print_high ('Scheduler init done')


    # Implemented as a callback function
    def start_streaming_cb (self):
        log.print_high ('Starting camera...')
        if (self.__cam.start_camera ('320x240', '5', 'night')):
            self.__pitft.Backlight (True)
            log.print_high ('scheduler: Starting stream_video_to_display...')
            self.__pitft.stream_video_to_display ()
        else:
            log.print_high ('scheduler: Camera already on')

    def stop_streaming_cb (self):

        log.print_high ('Stopping stream...')
        self.__pitft.stop_stream_video_to_display ()
        log.print_high ('Stream stoppped. Turning backlight off...')
        self.__pitft.Backlight (False)
        log.print_high ('Backlight off. Stopping camera...')
        
        if (self.__cam.stop_camera ()):
            log.print_high ('scheduler: Camera off')
        else:
            log.print_high ('scheduler: Could not turn off camera')
        log.print_high ('exiting inside_pir_triggered_callback')

    # Default schedule delay is 0 minutes
    def schedule_start_streaming (self, delay = 0):
        if (delay == 0):
            start_streaming_cb ()
        return

    # Default schedule delay is 4 minutes
    def schedule_stop_streaming (self, seconds_delay = 240):
        
        # Blindly cancel the job before scheduling it
        self.__stream_job.cancel_job ()
        self.__stream_job = self.__sched.add_job(stop_streaming_cb, datetime.datetime.today () + datetime.timedelta (seconds = seconds_delay))
        log.print_high ('Will turn off stream after ' + str (seconds_delay) + ' from now')
        return
