#!/usr/bin/python

# pyGraphite.py 
# 
# This python script is full of common functions that can be 
# imported for use in python scripts. 
# 
# Called on its own, it can be used to insert statistics from
# a shell script (or whatever else) thusly: 
#
# $ pyGraphite.py "CCIS.systems.<full path to stat>" <statistic>
#


import socket
import time
import argparse

graphiteServer = "YOURGRAPHITESERVER"
graphitePort = "2003"
usePickle = False #not supported yet
sock = socket.socket()

def connect(remServer=graphiteServer, remPort=int(graphitePort)):
	if (type(remServer) != str):
		print "Error: remServer should be a string"
		print type(remServer)
		exit()
	if (type(remPort) != int):
		print "Error: remPort should be an integer"
		print type(remPort)
		exit()
	sock.connect((remServer, remPort))

def sendData(metricPath, metricValue, metricTime = int(time.time())):
	if (type(metricTime) != int):
		print 'Error: metricTime needs to be an integer'
		print 'Instead, got ' + metricTime
		disconnect()
		exit()
	message = metricPath + " " + str(metricValue) + " " + str(metricTime) + "\n"
	sock.sendall(message)

def disconnect():
	sock.close()

def sendGraphite(metricPath, metricValue, metricTime = int(time.time())):
	# This is a wrapper script that does the individual steps for you. 
	# The only time you wouldn't want to use this is if you wanted 
	# to send multiple metrics from within another python script
	# by calling sendData() multiple times before disconnect()
	connect()
	sendData(metricPath, metricValue, metricTime)
	disconnect()

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Send data to graphite.')
	parser.add_argument('metricPath', action='store', help='Metric Path to store in graphite')
	parser.add_argument('metricValue', action='store', help='Metric Value to record')
	parser.add_argument('metricTime', action='store', help='(optional) timestamp to record', type=int, nargs='?')
	args = parser.parse_args()

	if ( args.metricTime ): 
		sendGraphite(metricPath = args.metricPath, metricValue = args.metricValue, metricTime = args.metricTime)
	else:
		sendGraphite(metricPath = args.metricPath, metricValue = args.metricValue)



