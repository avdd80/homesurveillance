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

#------------------------------------------------------#
#--------------------- ADDRESSES ----------------------#
#------------------------------------------------------#
    def get_cam_server_ip (self):
        return self.__address_node[0][0].text
#------------------------------------------------------#
    def get_cam_server_port (self):
        return self.__address_node[0][1].text
#------------------------------------------------------#
    def get_remote_cam_server_ip (self):
        return self.get_cam_server_ip ()
#------------------------------------------------------#
    def get_remote_cam_server_port (self):
        return self.get_cam_server_ip ()
#------------------------------------------------------#
    def get_instapush_notif_ip (self):
        return self.__address_node[1][0].text
#------------------------------------------------------#
    def get_instapush_notif_port (self):
        return self.__address_node[1][1].text
#------------------------------------------------------#        
    def get_display_stream_launcher_ip (self):
        return self.__address_node[2][0].text
#------------------------------------------------------#
    def get_display_stream_launcher_port (self):
        return self.__address_node[2][1].text
#------------------------------------------------------#
#----------------------- PATHS ------------------------
#------------------------------------------------------#
    def get_mjpg_streamer_path (self):
        return self.__path_node[0].text
#------------------------------------------------------#
