﻿from plugwise import *
from nexmomessage import NexmoMessage
from datetime import datetime
import ConfigParser
from collections import deque

class Appliance:
    def __init__(self, mac, sms_name):
        self.mac = mac
        self.sms_name = sms_name
        self.measures = deque([],100)
        self.cycle = False

    def HasCycleStarted(self, power_usage):
        return False
    def HasCycleEnded(self):
        return False      
    def Measure(self):
        try: 
            power_usage = self.c.get_power_usage()
        except Exception as e:
            print "Could not measure from " + self.sms_name + ":" + e.message
            return

        self.measures.append(power_usage)
        avg_m = sum(self.measures)/len(self.measures)

        if (not self.cycle and self.HasCycleStarted(power_usage, avg_m)):
            self.cycle = True
            self.cyclestarttime = datetime.now()
            appliance_started(self)
        if (self.cycle and self.HasCycleEnded(power_usage, avg_m)):
            self.cycle = False
            appliance_finished(self)

class Washer(Appliance):
	def HasCycleStarted(self, avg_m, power_usage):
		return power_usage > 50 and len(self.measures) > 60 and avg_m > 10
	def HasCycleEnded(self, avg_d, power_usage):
		return power_usage < 50 and len(self.measures) > 60 and avg_d < 10

class Dryer(Appliance):
	def HasCycleStarted(self, avg_m, power_usage):
		return power_usage > 50 and len(self.measures) > 60 and avg_m > 20
	def HasCycleEnded(self, avg_d, power_usage):
		return power_usage < 50 and len(self.measures) > 60 and avg_d < 20

def read_config():
    config = ConfigParser.RawConfigParser()
    config.read('config.cfg')
    device_section_names = config.get('Devices', 'keys').split(',')

    for device_section in device_section_names:
        mac = config.get(device_section, 'mac')
        sms_name = config.get(device_section, 'sms_name')
        type = config.get(device_section, 'type')
        if (type == 'Washer'):
            app = Washer(mac, sms_name)
        elif (type == 'Dryer'):
            app = Dryer(mac, sms_name)
        apps.append(app)

    numbers = config.options('Numbers')
    for number in numbers:
        sms_numbers.append(config.get('Numbers', number))

	nexmo_key = config.get('Nexmo', 'key')
	nexmo_secret = config.get('Nexmo', 'secret')
		

def send_sms(from_, text):
    for number in sms_numbers:
        msg = {
            'reqtype': 'json',
            'api_key': '17ab498d',
            'api_secret': '89df51fb',
            'from': from_,
            'to': number,
            'text': text
        }

        sms = NexmoMessage(msg)
        sms.set_text_info(msg['text'])
        print msg
        sms.send_request()

def appliance_started( sender ):
    print sender.sms_name, 'has started'
    now = datetime.now()
    send_sms(sender.sms_name, 'Startar nu (' + now.strftime('%H:%M') + ')')

def appliance_finished( sender ):
    print sender.sms_name, 'has ended'

    now = datetime.now()
    took_time = now - sender.cyclestarttime

    send_sms(sender.sms_name, 'Färdig! Tog ' +  ':'.join(str(took_time).split(':')[:2]) + ', slutade ' + now.strftime('%H:%M'))


apps = []
sms_numbers = []
nexmo_key = ''
nexmo_secret = ''
com_port = 'COM3'

read_config()


try:
    device = Stick(com_port)
except Exception as e:
    print "Could not connect to stick on port (" + com_port + "):", e.message
    sys.exit(1)

for app in apps:
	app.c = Circle(app.mac, device)

while True:
    for app in apps:
        app.Measure()
    time.sleep(1)
