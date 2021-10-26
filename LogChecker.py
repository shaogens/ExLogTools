#
# Constantly check client log for changes to pull
#

import time
import os

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

if __name__ == '__main__':
    logfile = open("D:/Steam/steamapps/common/Conan Exiles/ConanSandbox/Saved/Logs/ConanSandbox.log","r")
    loglines = follow(logfile)
    for line in loglines:
    	# need to detect rightline first
    	split = line.split(' ')
    	if "was hit by" in line:
    		print("DMG: {0} PEN: {1} ARM: {2}".format(split[11],split[13],split[17]))
    		#print("DMG: {0}".format(split[11]))
    		#print(repr(split))
        #print(line, end='')