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

		#[2021.11.11-13.54.11:124][503]Combat: [HumanoidNPCCharacter_C_807] DEBUG: Darfari Fighter II was hit by BasePlayerChar_C_0 using sword2h_C_2 for 13 with 0 penetration against my 66.25 armor value.
		#[2021.10.21-18.58.12:079][261]Combat: [HumanoidNPCCharacter_C_43] DEBUG: XX_DoNothingHealthBoost was hit by BasePlayerChar_C_0 using BP_Base_Visual_Axe2h_C_1 for 39 with 1 penetration against my 12.5 armor value.

		for line in loglines:
			split = line.split(' ')
			if "was hit by" in line:
				#split1 = line.split('DEBUG: ')
				#pre = split1[0]
				#post = split1[1]
				#split2 = post.split(' ')

				# this will match NPCs with 2-3 words in the name
				NeoSplit = re.findall(r'(\w+)?(?(3)\w+|) (\w+)?(?(3)\w+|) (\w+) was hit by (\w+) using (\w+) for (\d+) with (\d+) penetration against my (\d+)',line)
				print("Split 1: {0}".format(NeoSplit))
				if not NeoSplit:
					# Try again for a single-word name:
					NeoSplit = re.findall(r'(\w+) was hit by (\w+) using (\w+) for (\d+) with (\d+) penetration against my (\d+)',line)
					print("Split 2: {0}".format(NeoSplit))
					NPC = NeoSplit[0][0]
					Player = NeoSplit[0][1]
					WeaponBP = NeoSplit[0][2]
					Damage = NeoSplit[0][3]
					Penetration = NeoSplit[0][4]
					Armor = NeoSplit[0][5]
				else:
					# We have a 2-3 word named NPC
					if not NeoSplit[0][0]:
						# No word here, so its a two-word name
						NPC = NeoSplit[0][1] + ' ' + NeoSplit[0][2]
					else:
						NPC = NeoSplit[0][0] + ' ' + NeoSplit[0][1] + ' ' + NeoSplit[0][2]

					Player = NeoSplit[0][3]
					WeaponBP = NeoSplit[0][4]
					Damage = NeoSplit[0][5]
					Penetration = NeoSplit[0][6]
					Armor = NeoSplit[0][7]


				#print(NPC + ' ' + Player + ' ' + Damage + "\n")

	    		# matches 2 or 3 words
	    		# NeoSplit = re.findall(r'(\w+)?(?(3)\w+|) (\w+)?(?(3)\w+|) (\w+) was hit by (\w+)',line)
	    		# [('Darfari', 'Archer', 'III', 'BasePlayerChar_C_0')]
	    		# [('', 'Cannibal', 'Brute', 'BasePlayerChar_C_0')]

	    		# WORKS only w/ 3parters : NeoSplit = re.findall(r'DEBUG\: (\w+ \w+ \w+) was hit by (\w+)',line)
	    		#NeoSplit = re.findall(r'DEBUG\: [(\w+)] [(\w+)] (\w+) was hit by (\w+)',line)
	    		#Neo Split: [('Darfari Fighter I', 'BasePlayerChar_C_0')]

	    		# SORTA: NeoSplit = re.findall(r'DEBUG\: ([A-z]+) was hit by (\w+)',line)
	    		#Neo Split: [('XX_DoNothingHealthBoost', 'BasePlayerChar_C_0')]

	    		#NeoSplit = re.findall(r'(\w+): (\s*)',line)

	    		#print("LINE:")
	    		#print(repr(line))
	    		#print("Neo Split: ")
	    		#print(repr(NeoSplit))

				#
				
				if int(Damage) > self.lastHigh:
					self.lastHigh = int(Damage)
				
				if int(Damage) < self.lastLow:
					self.lastLow = int(Damage)

	    		#window['LogOutput'].print("DMG: {0} [Lo:{1}/Hi:{2}] PEN: {3} ARM: {4} Visual: {5}".format(hit,self.lastLow,self.lastHigh,split2[10],split2[14],split2[6]))
				window['LogOutput'].print("D: {0} [Lo:{1}/Hi:{2}] P: {3} A: {4} -- {5} Hit {6} with {7}".format(Damage,self.lastLow,self.lastHigh,Penetration,Armor,Player,NPC,WeaponBP))
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
