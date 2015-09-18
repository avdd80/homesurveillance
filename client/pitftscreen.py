'''
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.
'''

'''
Python module for Adafruit PiTFT by elParaguayo.

Initialises GPIO for all 4 tactile buttons.
Can also be used to turn backlight on or off.
'''

import RPi.GPIO    as     GPIO
from   time        import sleep
from   os          import system
from   os.path     import exists
from   commands    import getoutput
from   xml_handler import XML_Object
from   logger      import log_handler
from   subprocess  import Popen, PIPE

# Set log level to LOW
log = log_handler (True)
log.set_log_level (log.LOG_LEVEL_LOW)

def is_process_running (process_name):
    process_list = getoutput('ps -A')
    if ((process_name in process_list) or (process_name in process_list)):
        return True
    else:
        return False

class PiTFT_Screen(object):

    def __init__(self, v2 = True, buttons = [True, True, True, True]):
        '''Initialise class.

        v2 = True - if using older (v1) revision of board this should be
        set to False to ensure button 3 works correctly.

        buttons = [button1, button2, button3, button4] if you don't want to initialise
        any of the buttons then set the appropriate flag to False. Defaults to all
        buttons being initialised.

        NB. this class does not handle debouncing of buttons.
        '''

        log.print_high ('Setting up PiTFT...')

        # Set up some useful properties
        self.backlightpath = "/sys/class/gpio/gpio508"
        self.__b1 = False
        self.__b2 = False
        self.__b3 = False
        self.__b4 = False
        self.__pin1 = 23
        self.__pin2 = 22
        self.__pin3 = 27
        self.__pin4 = 18

        # set GPIO mode
        GPIO.setmode(GPIO.BCM)


        # Initialise buttons
        if buttons[0]:
            GPIO.setup(self.__pin1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            self.__b1 = True

        if buttons[1]:
            GPIO.setup(self.__pin2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            self.__b2 = True

        if buttons[2]:
            if not v2:
                self.__pin3 = 21

            GPIO.setup(self.__pin3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            self.__b3 = True

        if buttons[3]:
            GPIO.setup(self.__pin4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            self.__b4 = True

        # Try to set up the backlights
        self.backlightenabled = self.__setupBacklight()

        # If the set up worked it can default to turnng light off
        # so let's turn it back on
        if self.backlightenabled:
            self.Backlight(False)
        else:
            log.print_error ('Could not setup backlight')
            
        log.print_high ('PiTFT setup done')

    def __setupBacklight(self):

        log.print_high ('Setting up backlight')
        # Check if GPIO508 has already been set up
        if not exists(self.backlightpath):
            system("sudo sh -c 'echo 508 > /sys/class/gpio/export'")
        # Set the direction
        system("sudo sh -c 'echo out > /sys/class/gpio/gpio508/direction'")

        # If we had no errors up to here then we should be able to control
        # backlight
        return True

    def Backlight(self, light):
        '''Turns the PiTFT backlight on or off.

        Usage:
         Backlight(True) - turns light on
         Backlight(False) - turns light off
        '''
        log.print_high ('Inside backlight light = ' + str (light))
        

        if (light):
            log.print_low ('pitft: Backlight: Turning on display')
            #system ('sudo sh -c ''echo 1 > /sys/class/gpio/gpio508/value''')
            system ('sudo sh -c ''./display_on.sh''')

        else:
            log.print_low ('pitft: Backlight: Turning off display')
            #system ('sudo sh -c ''echo 0 > /sys/class/gpio/gpio508/value''')
            system ('sudo sh -c ''./display_off.sh''')


    # Add interrupt handling...
    def Button1Interrupt(self,callback=None,bouncetime=200):
        if self.__b1:
            GPIO.add_event_detect(self.__pin1,
                                  GPIO.FALLING,
                                  callback=callback,
                                  bouncetime=bouncetime)

    def Button2Interrupt(self,callback=None,bouncetime=200):
        if self.__b2:
            GPIO.add_event_detect(self.__pin2,
                                  GPIO.FALLING,
                                  callback=callback,
                                  bouncetime=bouncetime)

    def Button3Interrupt(self,callback=None,bouncetime=200):
        if self.__b3:
            GPIO.add_event_detect(self.__pin3,
                                  GPIO.FALLING,
                                  callback=callback,
                                  bouncetime=bouncetime)

    def Button4Interrupt(self,callback=None,bouncetime=200):
        if self.__b4:
            GPIO.add_event_detect(self.__pin4,
                                  GPIO.FALLING,
                                  callback=callback,
                                  bouncetime=bouncetime)

    def stream_video_to_display (self):
        log.print_high ('pitft: stream_video_to_display: Entered')
        xml = XML_Object ()
        tcp_ip   = xml.get_remote_cam_server_ip ()
        tcp_port = xml.get_remote_cam_server_port ()
        timeout = 10
        log.print_high ('Starting omxplayer')
        Popen('/usr/bin/omxplayer --live --fps 10 http://' + str (tcp_ip) + ':' + str (tcp_port) + '/?action=stream', shell=True, stdout=PIPE)
        sleep (0.1)
        # Check if the process is running. If not, restart the process
        while (((is_process_running ('omxplayer.bin') == False) and (is_process_running ('omxplayer') == False)) and (timeout > 0)):
            Popen('/usr/bin/omxplayer --live --fps 10 http://' + str (tcp_ip) + ':' + str (tcp_port) + '/?action=stream', shell=True, stdout=PIPE)
            timeout = timeout - 1
            log.print_high ('Starting omxplayer. Number retries left: ' + str(timeout))
            sleep (0.5)
        log.print_high ('pitft: stream_video_to_display: Exit')
            
    def stop_stream_video_to_display (self):
        log.print_high ('pitft: stop_stream_video_to_display: Entered')
        timeout = 10
        log.print_high ('Killing omxplayer')
        Popen ('sudo pkill omxplayer'    , shell=True, stdout=PIPE)
        Popen ('sudo pkill omxplayer.bin', shell=True, stdout=PIPE)
        sleep (0.1)
        while (((is_process_running ('omxplayer.bin') == True) or (is_process_running ('omxplayer') == True)) and timeout > 0):
            Popen ('sudo pkill omxplayer', shell=True, stdout=PIPE)
            Popen ('sudo pkill omxplayer.bin', shell=True, stdout=PIPE)
            timeout = timeout - 1
            log.print_high ('Killing omxplayer. Number retries left: ' + str(timeout))
            sleep (0.2)
        log.print_high ('pitft: stop_stream_video_to_display: Exit')


    # Include the GPIO cleanup method
    def Cleanup(self):
        GPIO.cleanup()


    # Some properties to retrieve value state of pin and return more logical
    # True when pressed.
    @property
    def Button1(self):
        '''Returns value of Button 1. Equals True when pressed.'''
        if self.__b1:
            return not GPIO.input(self.__pin1)

    @property
    def Button2(self):
        '''Returns value of Button 2. Equals True when pressed.'''
        if self.__b2:
            return not GPIO.input(self.__pin2)

    @property
    def Button3(self):
        '''Returns value of Button 3. Equals True when pressed.'''
        if self.__b3:
            return not GPIO.input(self.__pin3)

    @property
    def Button4(self):
        '''Returns value of Button 4. Equals True when pressed.'''
        if self.__b4:
            return not GPIO.input(self.__pin4)


