#
# Core functions
#
import threading
import os, time
import PySimpleGUI as sg

xEvent = 0

def toggle_xEvent(value,event):

	if value == "start":
		xEvent = event
	elif value == "stop":
		capture_stop(x,xEvent)

def follow(thefile,keepalive):
	# Constantly check logfile for changes
	thefile.seek(0, os.SEEK_END)
		
	while keepalive:
		if xEvent.is_set():
			keepalive = False
		line = thefile.readline()
		if not line:
			time.sleep(0.1)
			continue
		yield line

def capture_log(window,logpath,keepalive):
	# Capture log output
    logfile = open(logpath,"r")
    keepalive = True
    loglines = follow(logfile,keepalive)
    
    lastLow = 10000
    lastHigh = 0
    #print ('For Start...')
    LogReport = []
    for line in loglines:
    	# Need way to detect and break this when needed
    	#  Looks like will need to stop the loop in follow()
    	
    	split = line.split(' ')
    	#print(repr(split))
    	if "was hit by" in line:
    		split1 = line.split('DEBUG: ')
    		pre = split1[0]
    		post = split1[1]
    		split2 = post.split(' ')
    		
    		hit = int(split2[8])
    		
    		if hit > lastHigh:
    			lastHigh = hit
    		
    		if hit < lastLow:
    			lastLow = hit
    		
    		LogReport.append("DMG: {0} [hi:{1}/lo:{2}] PEN: {3} ARM: {4} Visual: {5}".format(hit,lastHigh,lastLow,split2[10],split2[14],split2[6]))
    		#print("DMG: {0} [hi:{1}/lo:{2}] PEN: {3} ARM: {4} Visual: {5}".format(hit,lastHigh,lastLow,split2[10],split2[14],split2[6]))
    		window['LogOutput'].update(values=(LogReport))

def capture_start(window,logpath,keepalive):
	# Start capturing
	xEvent = threading.Event()
	x = threading.Thread(target=capture_log, args=(window,logpath,True,))
	x.start()
	
	return x, xEvent
	
def capture_stop(x,xEvent):
	# Stop Capturing
	print("Setting event")
	xEvent.set()
	
	if xEvent.is_set():
		print("Event is set true")
