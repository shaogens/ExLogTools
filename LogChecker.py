#
# Constantly check client log for changes to pull
#

import time
import os
#import keyboard
#import threading

# Combat Log references:
# [2021.10.21-18.58.12:079][261]Combat: [HumanoidNPCCharacter_C_43] DEBUG: XX_DoNothingHealthBoost was hit by BasePlayerChar_C_0 using BP_Base_Visual_Axe2h_C_1 for 39 with 1 penetration against my 12.5 armor value.
# [2021.10.21-18.58.12:079][261]Combat: [HumanoidNPCCharacter_C_43] DEBUG: BasePlayerChar_C_0 has knockback BP_Base_Visual_Axe2h_C_1 with 10.0 in direction NN.
# [2021.10.21-18.58.12:080][261]Combat: [BP_Base_Visual_Axe2h_C_1] DEBUG - Durability changed on [Axe of the Adventurer] by [-1] to [2016.800049/2060.800049]

# https://github.com/dabeaz/generators/blob/master/examples/follow.py
def follow(thefile):
    thefile.seek(0, os.SEEK_END)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

# Example use
# Note : This example requires the use of an apache log simulator.
# 
# Go to the directory run/foo and run the program 'logsim.py' from
# that directory.   Run this program as a background process and
# leave it running in a separate window.  We'll write program
# that read the output file being generated
# 

def tail_log(logpath):
    logfile = open(logpath,"r")
    loglines = follow(logfile)
    
    lastLow = 10000
    lastHigh = 0
    print ('For Start...')
    for line in loglines:
    	# need to detect rightline first
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
    		
    		
    		print("DMG: {0} [hi:{1}/lo:{2}] PEN: {3} ARM: {4} Visual: {5}".format(hit,lastHigh,lastLow,split2[10],split2[14],split2[6]))
	

# logpath = "E:/Games/SteamSSD/steamapps/common/Conan Exiles/ConanSandbox/Saved/Logs/ConanSandbox.log"
#logpath = "D:/SteamD/steamapps/common/Conan Exiles/ConanSandbox/Saved/Logs/ConanSandbox.log"
logpath = "D:/Steam/steamapps/common/Conan Exiles/ConanSandbox/Saved/Logs/ConanSandbox.log"

if __name__ == '__main__':
	# E:/Games/SteamSSD/steamapps/common/Conan Exiles/ConanSandbox/Saved/Logs
	#x = threading.Thread(target=tail_log, args=(logpath,))
	#x.start()
	tail_log(logpath)
	
	
	#while x.is_alive():
		#if keyboard.read_key() == "r":
	#	if keyboard.is_pressed("r"):
	#		print("R pressed")
	#		break
		#elif keyboard.read_key() == "q":
	#	if keyboard.is_pressed("q"):
	#		print("Quitting!")
	#		exit()

    		# split2 0 = Attackee
    		# 		 4 = Attacker
    		#		 6 = Weapon used (Visual Object)

        #print(line, end='')
        
        
#['XX_DoNothingHealthBoost', 'was', 'hit', 'by', 'BasePlayerChar_C_0', 'using', 'sword2h_legendary_glow_C_0', 'for', '114', 'with', '0.764', 'penetration', 'against', 'my', '12.5', 'armor', 'value.\n']
#DMG: 114 PEN: 0.764 ARM: 12.5

#['XX_DoNothingHealthBoost', 'was', 'hit', 'by', 'BasePlayerChar_C_0', 'using', 'sword2h_legendary_glow_C_0', 'for', '87', 'with', '0.764', 'penetration', 'against', 'my', '12.5', 'armor', 'value.\n']
#DMG: 87 PEN: 0.764 ARM: 12.5