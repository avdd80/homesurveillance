# -----------------------------------------------------#
#!/usr/bin/python
# xml_handler.py
# XML settings file handler
# -----------------------------------------------------#
import xml.etree.ElementTree as ET

class XML_Object(object):

    def __init__(self):
    
        self.__xml_path     = '../settings.xml'
        self.__tree         = ET.parse (self.__xml_path)
        self.__root         = self.__tree.getroot ()
        self.__address_node = self.__root[0]
        self.__path_node    = self.__root[1]
        self.__gpio_node    = self.__root[2]
        self.__timings_node = self.__root[3]
        self.__clients_node = self.__address_node
        self.__misc_node    = self.__root[5]

#------------------------------------------------------#
#--------------------- ADDRESSES ----------------------#
#------------------------------------------------------#
#-- CAM SERVER ----------------------------------------#
    def get_cam_server_ip (self):
        return self.__address_node[0][0].text
#------------------------------------------------------#
    def get_cam_server_port (self):
        return int (self.__address_node[0][1].text)
#------------------------------------------------------#
    def get_remote_cam_server_ip (self):
        return self.get_cam_server_ip ()
#------------------------------------------------------#
    def get_remote_cam_server_port (self):
        return self.get_cam_server_port ()
#------------------------------------------------------#
#-- INSTAPUSH -----------------------------------------#
    def get_instapush_notif_ip (self):
        return self.__address_node[1][0].text
#------------------------------------------------------#
    def get_instapush_notif_port (self):
        return int (self.__address_node[1][1].text)
#------------------------------------------------------#
#-- DISPLAY STREAM ------------------------------------#
    def get_display_stream_launcher_ip (self):
        return self.__address_node[2][0].text
#------------------------------------------------------#
    def get_display_stream_launcher_port (self):
        return int (self.__address_node[2][1].text)
#------------------------------------------------------#
#-- JOB SCHEDULER -------------------------------------#
    def get_job_scheduler_ip (self):
        return self.__address_node[3][0].text
#------------------------------------------------------#
    def get_job_scheduler_port (self):
        return int (self.__address_node[3][1].text)
#------------------------------------------------------#
#----------------- REMOTE CLIENTS ---------------------#
#------------------------------------------------------#
    def get_client_count (self):
        return int (self.__misc_node[0].text)
#------------------------------------------------------#
    def get_client_ip (self, client_number):
        if (client_number < self.get_client_count ()):
            return self.__clients_node[0][0].text
        else:
            print 'Specified client number ' + str (client_number) + ' exceeds registered number of clients = ' + str (self.get_client_count ())
            exit ()
#------------------------------------------------------#
    def get_client_port (self, client_number):
        if (client_number < self.get_client_count ()):
            return int (self.__clients_node[0][1].text)
        else:
            print 'Specified client number ' + str (client_number) + ' exceeds registered number of clients = ' + str (self.get_client_count ())
            exit ()
#------------------------------------------------------#
    def get_client_display_type (self, client_number):
        if (client_number < self.get_client_count ()):
            return self.__clients_node[1].text
        else:
            print 'Specified client number ' + str (client_number) + ' exceeds registered number of clients = ' + str (self.get_client_count ())
            exit ()
#------------------------------------------------------#
#----------------------- GPIO -------------------------#
#------------------------------------------------------#
    def get_inside_pir_gpio_pin (self):
        return int (self.__gpio_node[0].text)
#------------------------------------------------------#
    def get_outside_pir_gpio_pin (self):
        return int (self.__gpio_node[1].text)
#------------------------------------------------------#
    def get_door_switch_gpio_pin (self):
        return int (self.__gpio_node[2].text)
#------------------------------------------------------#
#--------------------- Timings ------------------------#
#------------------------------------------------------#
    def get_instapush_notif_timeout (self):
        return int (self.__timings_node[0].text)
#------------------------------------------------------#
    def min_gap_between_two_instapush_notif (self):
        return int (self.__timings_node[1].text)
#------------------------------------------------------#
#----------------------- Misc -------------------------#
#------------------------------------------------------#
    def get_instapush_notif_interrupt_count (self):
        return int (self.__misc_node[1].text)
#------------------------------------------------------#
#------------------------------------------------------#
#------------------------------------------------------#
#----------------------- PATHS ------------------------
#------------------------------------------------------#
    def get_mjpg_streamer_path (self):
        return self.__path_node[0].text
#------------------------------------------------------#
