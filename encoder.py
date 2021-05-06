#!/usr/bin/env python

import os
import sys
import requests

if not os.getegid() == 0:
    sys.exit('Script must be run as root')

from time import sleep
from pyA20.gpio import gpio
from pyA20.gpio import connector
from pyA20.gpio import port

handle = open("encoder.set", "r")
server = (handle.readline()).strip()
player = (handle.readline()).strip()
volstep = int( (handle.readline()).strip() )
print(server, player, volstep)
handle.close()

"""Init gpio module"""
gpio.init()

volume = 0

"""Set directions"""
g3 = connector.gpio1p3
g5 = connector.gpio1p5
g7 = connector.gpio1p7
print g3, g5, g7

gpio.setcfg(g3, gpio.INPUT)
gpio.setcfg(g5, gpio.INPUT)
gpio.setcfg(g7, gpio.INPUT)
print (gpio.input(g3), gpio.input(g5), gpio.input(g7))
#sleep(5)

"""Enable pullup resistor"""
gpio.pullup(g3, 0)   #Clear pullups
gpio.pullup(g5, 0)
gpio.pullup(g7, 0)

gpio.pullup(g3, gpio.PULLUP)
gpio.pullup(g5, gpio.PULLUP)
gpio.pullup(g7, gpio.PULLUP)

response = 1

try:
    print ("Encoder started! Press CTRL+C to exit")
    while True:
	if gpio.input(g3) == 0 and gpio.input(g5) <> 0:
		volume = volume + volstep
		response = requests.get('http://'+server+':9000/status.html', params={'p0': 'mixer', 'p1': 'volume', 'p2': '+5', 'player': player},)
		print ('up', volume, server, player, response)
		sleep(0.01)
	if gpio.input(g5) == 0 and gpio.input(g3) <> 0:
                volume = volume - volstep
		response = requests.get('http://'+server+':9000/status.html', params={'p0': 'mixer', 'p1': 'volume', 'p2': '-5', 'player': player},)
		print ('dn', volume, server, player, response)		
		sleep(0.01) 
	if gpio.input(g7) == 0:
                volume = volume - volstep
                response = requests.get('http://'+server+':9000/status.html', params={'p0': 'pause', 'player': player},)
                print ('pause', volume, server, player, response)
                sleep(0.01)
#print server, player, volume
        sleep(0.001)

except KeyboardInterrupt:
    print ("Goodbye.")
