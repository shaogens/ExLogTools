#
# Exiles Log Tools
#
# Stuff for processing the conan log file in real time.

import PySimpleGUI as sg
import ctypes
import platform
from main import ExiLogger
from jparse import jconf

VERSION = "1.1"

def make_dpi_aware():
	# Fix blurry text on high dpi monitors
	# reqs: ctypes, platform
	# https://github.com/PySimpleGUI/PySimpleGUI/issues/1179
    if int(platform.release()) >= 8:
        ctypes.windll.shcore.SetProcessDpiAwareness(True)
        
OutVals = ""
Logging = 0
capture = False

# If json file exists, grab last used log path
config = jconf()
LogPath = config.config("LogPath")
#print("Startup Log Path")
#print(repr(LogPath))

        
Layout = [
		[sg.Text("Log File:"),sg.Input(LogPath,size=(80,0),key="LogPath"),sg.FileBrowse(file_types=(("Log Files","*.log"),)),sg.Button("About",key="About")],
		[sg.Button("Start Capture",key="CaptureToggle"),sg.Text("  "),sg.Button("Reset Counters",key="CounterClear"),sg.Button("Clear Window",key="WindowClear")],
		[sg.Text("Combat Log:")],
		[sg.Multiline(size=(100,20),autoscroll=True,write_only=True,disabled=True,key="LogOutput")]
		#[sg.Listbox(values=(OutVals),size=(100,20),enable_events=True,key="LogOutput")]
	]
        
	
make_dpi_aware()

sg.theme('DarkBlue13')
window = sg.Window("Exile Log Tools", Layout,).Finalize()

while True:
	event, values = window.read()
	
	if event == "CounterClear":
		# Clear Counters
		Logging.ResetCounters(window)
		
	elif event == "WindowClear":
		# Clear log in window
		Logging.ClearWindow(window)
		
	elif event == "CaptureToggle":
		# Toggle between starting/stopping capture of log
		
		if capture == False:
			# Start
			Logging = ExiLogger()
			Logging.start(window,values['LogPath'],True)
			# Rename button to stop			
			window['CaptureToggle'].update("Stop Capture")			
			capture = True
			updateret = config.update("Config",{"LogPath": values['LogPath']})
		elif capture == True:
			Logging.stop()
			window['CaptureToggle'].update("Start Capture")		
			capture = False
			
	elif event == "About":
		sg.popup("Exile Log Tools","Version: " + VERSION)
		
	elif event == sg.WIN_CLOSED:
		break
	
winret = window.close()
if capture == True:
	# Insure logging has stopped when closing to prevent app from becoming a zombie
	Logging.stop()

