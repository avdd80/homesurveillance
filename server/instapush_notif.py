import pycurl, json
from StringIO import StringIO
import time
from  socket import *
from logger import log_handler
from xml_handler import XML_Object

xml = XML_Object ()

HOST    = xml.get_instapush_notif_ip ()
RX_PORT = xml.get_instapush_notif_port ()
RX_ADDR = (HOST, RX_PORT)
BUFSIZE = 256

udp_recv_client = socket( AF_INET,SOCK_DGRAM)
udp_recv_client.setsockopt (SOL_SOCKET, SO_REUSEADDR, 1)
udp_recv_client.bind (RX_ADDR)

log = log_handler (True)
log.set_log_level (log.LOG_LEVEL_LOW)

#setup InstaPush variables
# add your Instapush Application ID
appID = "55f90a63a4c48a3b1f997fea"

# add your Instapush Application Secret
appSecret = "31fecf9743e4adffda5ae016c05f05bf"
pushEvent = "CamAlert"
pushMessage = "Door Opened!"

# use this to capture the response from our push API call
buffer = StringIO()

# use Curl to post to the Instapush API
c = pycurl.Curl()

# set API URL
c.setopt(c.URL, 'https://api.instapush.im/v1/post')

#setup custom headers for authentication variables and content type
c.setopt(c.HTTPHEADER, ['x-instapush-appid: ' + appID,
                        'x-instapush-appsecret: ' + appSecret,
                        'Content-Type: application/json'])


# create a dict structure for the JSON data to post
json_fields = {}

# setup JSON values
json_fields['event']=pushEvent
json_fields['trackers'] = {}

# set this so we can capture the resposne in our buffer
c.setopt(c.WRITEFUNCTION, buffer.write)

# uncomment to see the post sent
c.setopt(c.VERBOSE, True)


# setup an indefinite loop that looks for the door to be opened / closed
while True:

        pushMessage = udp_recv_client.recv(BUFSIZE)
        
        timenow24 = time.asctime ()
        timenow24 = time.strptime (timenow24[11:16],  "%H:%M")
        timenow12 = time.strftime( "%I:%M %p", timenow24 )

        pushMessage = '[' + timenow12 + '] ' + pushMessage

        json_fields['trackers']['message']=pushMessage
        #print(json_fields)
        postfields = json.dumps(json_fields)

        # make sure to send the JSON with post
        c.setopt(c.POSTFIELDS, postfields)


        # in the door is opened, send the push request
        c.perform()

        # capture the response from the server
        body= buffer.getvalue()

        # print the response
        print(body)

        # reset the buffer
        buffer.truncate(0)
        buffer.seek(0)

        print("Sent message: " + pushMessage)

        time.sleep (0.5)
