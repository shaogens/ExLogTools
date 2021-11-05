#
# Parsing of JSON files
#

import json
import os
from pathlib import Path

class jconf:

	data = ""

	def __init__(self):
		HomeDir = Path(__file__).parent
		SavesFile = HomeDir.joinpath('ExLogTools.json')
		if os.path.isfile(SavesFile):
			with open(SavesFile,'r') as f:
				self.data = json.load(f)
		else:
			#raise IOError
			print("jconf init else")
			# JSON File doesnt exist. create an empty file
			self.create()
			
	def create(self):
		# No json existed, so we're creating a new one
		print("jconf:create")
		
		#data = json.JSONEncoder().encode({"Config": [{"LogPath": "C:/"}]})
		data = {"Config": [{"LogPath": "C:/"}]}
		print("JSON: ")
		print(repr(data))
		
		HomeDir = Path(__file__).parent
		SavesFile = HomeDir.joinpath('ExLogTools.json')
		with open(SavesFile,'w') as f:
			json.dump(data,f,indent=4)		
			
	def refresh(self):
		# Reload the json file
		HomeDir = Path(__file__).parent
		SavesFile = HomeDir.joinpath('ExLogTools.json')
		with open(SavesFile,'r') as f:
			self.data = json.load(f)		
			
	def config(self,setting):
		# Pull up a setting
		ret = False
		for i in self.data['Config']:
			for i2 in i:
				if i == setting:
					ret = self.data['Config'][i]
		return ret
		
		
	def update(self,attr,val):
		self.data[attr] = val
		
		HomeDir = Path(__file__).parent
		SavesFile = HomeDir.joinpath('ExLogTools.json')
		with open(SavesFile,'w') as f:
			json.dump(self.data,f,indent=4)
		
		return True		
