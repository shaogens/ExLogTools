#
# Core functions, as a class
#
import threading
import os, time, re
import PySimpleGUI as sg

class ExiLogger:
	
	def follow(self,thefile,keepalive):
		# The actual monitoring of the log file
		
		# Constantly check logfile for changes
		thefile.seek(0, os.SEEK_END)
			
		while keepalive:
			if self.xEvent.is_set():
				keepalive = False
				#print("Keep Alive: FALSE")
			line = thefile.readline()
			if not line:
				time.sleep(0.1)
				continue
			yield line
			
	def start(self,window,logpath,keepalive):
		# Start capturing
		self.xEvent = threading.Event()
		self.x = threading.Thread(target=self.capture, args=(window,logpath,True,))
		self.x.start()
		
		return self.x, self.xEvent
		
	def stop(self):
		# Stop Capturing
		#print("Setting event")
		self.xEvent.set()
		
		#if self.xEvent.is_set():
			#print("Event is set true")
			
	def capture(self,window,logpath,keepalive):
	    logfile = open(logpath,"r")
	    keepalive = True
	    loglines = self.follow(logfile,keepalive)
	    
	    self.lastLow = 10000
	    self.lastHigh = 0
	    LogReport = []

	    for line in loglines:
	    	split = line.split(' ')
	    	if "was hit by" in line:
	    		split1 = line.split('DEBUG: ')
	    		pre = split1[0]
	    		post = split1[1]
	    		split2 = post.split(' ')
	    		
	    		hit = int(split2[8])
	    		
	    		if hit > self.lastHigh:
	    			self.lastHigh = hit
	    		
	    		if hit < self.lastLow:
	    			self.lastLow = hit
	    		
	    		#LogReport.append("DMG: {0} [Lo:{1}/Hi:{2}] PEN: {3} ARM: {4} Visual: {5}".format(hit,self.lastLow,self.lastHigh,split2[10],split2[14],split2[6]))
	    		#print("DMG: {0} [hi:{1}/lo:{2}] PEN: {3} ARM: {4} Visual: {5}".format(hit,lastHigh,lastLow,split2[10],split2[14],split2[6]))
	    		#window['LogOutput'].update(values=(LogReport))
	    		window['LogOutput'].print("DMG: {0} [Lo:{1}/Hi:{2}] PEN: {3} ARM: {4} Visual: {5}".format(hit,self.lastLow,self.lastHigh,split2[10],split2[14],split2[6]))
	    	elif "equipped" in line:
	    		# Weapon was [un]equipped
	    		split1 = line.split('DEBUG: ')
	    		pre = split1[0]
	    		post = split1[1]
	    		split2 = post.split(' ')
	    		
	    		# Split out whether the player is equipping or unequipping
	    		equip = split2[2]
	    		
	    		# Char name and Weapon name are in brackets (these names can have spaces)
	    		# so use regex to split them out
	    		repost = re.findall("\[(.*?)\]", post)
	    		
	    		window['LogOutput'].print("{0} {1} Weapon: {2}".format(repost[0],equip,repost[1]))
	    		#[2021.11.05-19.44.41:428][462]Combat: [BasePlayerChar_C_0] DEBUG: Actor [Shogen] unequipped [Obsidian Mace] weapon.
				#[2021.11.05-19.44.41:430][462]Combat: [BasePlayerChar_C_0] DEBUG: Actor [Shogen] equipped [Doom] weapon.
	    		

	def ResetCounters(self,window):
		#print("Reset Counters")
		self.lastHigh = 0
		self.lastLow = 10000
		window['LogOutput'].print("-- Counters Reset --")
		
	def ClearWindow(self,window):
		#print("Clear Window")
		LogReport = []
		window['LogOutput'].update("")
