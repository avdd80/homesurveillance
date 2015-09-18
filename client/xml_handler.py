import xml.etree.ElementTree as ET

class XML_Object(object):

    def __init__(self):
    
        self.__xml_path = '../settings.xml'
        self.__tree = ET.parse (self.__xml_path)
        self.__root = self.__tree.getroot ()
        self.__address_node = self.__root[0]


    def get_remote_cam_server_ip ():
        return self.__address_node[0][0].text
        
    def get_remote_cam_server_port ():
        return self.__address_node[0][1].text

    def get_instapush_notif_ip ():
        return self.__address_node[1][0].text

    def get_instapush_notif_port ():
        return self.__address_node[1][1].text
        
    def get_display_stream_launcher_ip ():
        return self.__address_node[2][0].text

    def get_display_stream_launcher_port ():
        return self.__address_node[2][1].text