#!/usr/bin/python
# sensors.py
# Python script to handle sensors
# -----------------------------------------------

import RPi.GPIO    as     GPIO
from   os.path     import exists
from   logger      import log_handler
from   xml_handler import XML_Object

log = log_handler (True)
log.set_log_level (log.LOG_LEVEL_LOW)

xml = XML_Object ()

class Sensors(object):

    def __init__(self, inside_pir_triggered_callback, outside_pir_triggered_callback,
                       door_switch_triggered_callback):
        '''
        Initialise class.
        '''
    
        # Self 
        # Set GPIO values for the connected hardware
        self.__pir_inside_gpio  = xml.get_inside_pir_gpio_pin ()
        self.__pir_outside_gpio = xml.get_outside_pir_gpio_pin ()
        self.__door_switch_gpio = xml.get_door_switch_gpio_pin ()
        
        log.print_low ('Sensors: init: set inside PIR GPIO = '  + str (self.__pir_inside_gpio))
        log.print_low ('Sensors: init: set outside PIR GPIO = ' + str (self.__pir_outside_gpio))
        log.print_low ('Sensors: init: set door GPIO = '        + str (self.__door_switch_gpio))


        # Add callbacks for interrupts
        self.__inside_PIR_triggered_callback  = inside_pir_triggered_callback
        self.__outside_PIR_triggered_callback = outside_pir_triggered_callback
        self.__door_switch_triggered_callback = door_switch_triggered_callback

        # set GPIO mode
        GPIO.setmode(GPIO.BCM)
        
        # Setup GPIOs for sensors
        GPIO.setup(self.__pir_inside_gpio,  GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.__pir_outside_gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.__door_switch_gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.enable_InsidePIRInterrupt ()
        self.enable_OutsidePIRInterrupt ()
        self.enable_DoorSwitchInterrupt ()

        log.print_high('Sensors: Init done')


    # Add interrupt handling...
    def enable_InsidePIRInterrupt(self,callback=None):
        GPIO.add_event_detect(self.__pir_inside_gpio,
                                  GPIO.FALLING,
                                  callback=self.__inside_PIR_triggered_callback,
                                  bouncetime=300)
        log.print_high ('InsidePIRInterrupt: Added a FALLING edge event')


    def enable_OutsidePIRInterrupt(self,callback=None):
        GPIO.add_event_detect(self.__pir_outside_gpio,
                                  GPIO.FALLING,
                                  callback=self.__outside_PIR_triggered_callback,
                                  bouncetime=300)
        log.print_high ('InsidePIRInterrupt: Added a RISING edge event')

    def enable_DoorSwitchInterrupt(self,callback=None):
        GPIO.add_event_detect(self.__door_switch_gpio,
                                  GPIO.FALLING,
                                  callback=self.__outside_PIR_triggered_callback,
                                  bouncetime=500)
        log.print_high ('InsidePIRInterrupt: Added a FALLING edge event')
        
        
    def disable_InsidePIRInterrupt (self, callback=None):
        GPIO.remove_event_detect(self.__pir_inside_gpio)
        log.print_high ('InsidePIRInterrupt: Disabled interrupt')

    def disable_OutsidePIRInterrupt (self, callback=None):
        GPIO.remove_event_detect(self.__pir_outside_gpio)
        log.print_high ('OutsidePIRInterrupt: Disabled interrupt')
        
    def disable_DoorSwitchInterrupt (self, callback=None):
        GPIO.remove_event_detect(self.__door_switch_gpio)
        log.print_high ('DoorSwitchInterrupt: Disabled interrupt')


    # Include the GPIO cleanup method
    def Cleanup(self):
        GPIO.cleanup()
        log.print_low ('pir: Cleanup')


#---------------------------------------------------------------------------

