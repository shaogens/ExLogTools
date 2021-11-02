#
# Parsing of JSON files
#

import json
import os
from pathlib import Path

class jconf:

	def __init__(self):
		HomeDir = Path(__file__).parent
		SavesFile = HomeDir.joinpath('ExLogTools.json')
		if os.path.isfile(SavesFile):
			with open(SavesFile,'r') as f:
				self.data = json.load(f)
		else:
			raise IOError
			
	def refresh(self):
		# Reload the json file
		HomeDir = Path(__file__).parent
		SavesFile = HomeDir.joinpath('ExLogTools.json')
		with open(SavesFile,'r') as f:
			self.data = json.load(f)		
			
	def config(self,setting):
		# Pull up a setting
		if setting == "all":
			ret = self.data['Config']
		else:
			for i in self.data['Config']:
				for i2 in i:
					if i2 == setting:
						ret = i[i2]
					
		return ret
		
	def maps(self,name):
		# Get list of maps
		# OR get just the filename for Map Name
		if name == "0":
			#Get all maps
			ret = {}
			for i in self.data['Maps']:
				ret[i['Name']] = i['FileName']
			return ret
		else:
			# looking for just a filename
			ret = True
			
	def saves(self,name):
		# Save Files
		if name == "saves-list":
			# return just the save name and associated map
			ret = []
			for i in self.data['Saves']:
				#ret[i['SaveName']] = i['Map']
				ret.append('[' + i['Map'] + '] ' + i['SaveName'])
		elif name == "saves-all":
			# Get full saves dictionary and return it
			ret = self.data['Saves']
		else:
			# get a specific save
			ret = {}
			for i in self.data['Saves']:
				for i2 in i:
					if i['SaveName'] == name:
						ret[i2] = i[i2]
						ret['Desc'] = i['Desc']
						ret['Map'] = i['Map']
						ret['FileName'] = i['FileName']
						ret['Hash'] = i['Hash']
						ret['SaveDate'] = i['SaveDate']
						ret['BranchName'] = i['BranchName']
			
		return ret
		
	def save_exist(self,dbhash):
		# Check if the given db file hash already exists
		print('DBHash: {0}'.format(dbhash))
		ret = {}
		for i in self.data['Saves']:
			for i2 in i:
				if i['Hash'] == dbhash:
					# Match
					print('Hash Match')
					ret['SaveName'] = i['SaveName']
					ret[i2] = i[i2]
		
		if len(ret) == 0:
			# No matches, be clear we're returning false
			ret = False
					
		return ret
		
		
	def update(self,attr,val):
		self.data[attr] = val
		
		HomeDir = Path(__file__).parent
		SavesFile = HomeDir.joinpath('ExCharPy.json')
		with open(SavesFile,'w') as f:
			json.dump(self.data,f,indent=4)
		
		return True		
