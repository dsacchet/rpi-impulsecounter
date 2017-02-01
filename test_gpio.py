#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import datetime
import subprocess
import sys
import json
import pprint

pp = pprint.PrettyPrinter(depth=6)

fread = open('/var/www/html/stat')
fcontent = fread.read()
fread.close()
data = json.loads(fcontent)

pp.pprint(data)

config = { 12 : "eau_chaude", 16 : "compteur_principal" }

def cb_eau(channel):
	global data
	now = datetime.datetime.now()
	heure = now.strftime('%Y-%m-%d %H:%M:%S.%f')
	current_value = data[config[channel]]
	data[config[channel]]=current_value+1
	output_json = json.dumps(data)
	fwrite = open('/var/www/html/stat','w')
	fwrite.write(output_json)
	fwrite.close()

GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.IN)
GPIO.add_event_detect(12, GPIO.RISING, callback=cb_eau, bouncetime=97)

GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.IN)
GPIO.add_event_detect(16, GPIO.RISING, callback=cb_eau, bouncetime=97)

while True:
	time.sleep(0.1)
