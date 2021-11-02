#
# Exiles Log Tools
#
# Stuff for processing the conan log file in real time.

import PySimpleGUI as sg
import ctypes
import platform
from main import ExiLogger
from jparse import jconf

def make_dpi_aware():
	# Fix blurry text on high dpi monitors
	# reqs: ctypes, platform
	# https://github.com/PySimpleGUI/PySimpleGUI/issues/1179
    if int(platform.release()) >= 8:
        ctypes.windll.shcore.SetProcessDpiAwareness(True)
        
OutVals = ""
#logThread = ""
Logging = 0
capture = False

config = jconf()
LogPath = config.config("LogPath")
        
Layout = [
		[sg.Text("Log File:"),sg.Input(LogPath,size=(80,0),key="LogPath"),sg.FileBrowse(file_types=(("Log Files","*.log"),))],
		[sg.Button("Start Capture",key="CaptureToggle"),sg.Text("  "),sg.Button("Reset Counters",key="CounterClear"),sg.Button("Clear Window",key="WindowClear")],
		[sg.Text("Combat Log:")],
		[sg.Listbox(values=(OutVals),size=(100,20),enable_events=True,key="LogOutput")]
	]
        
	
make_dpi_aware()

sg.theme('DarkBlue13')
window = sg.Window("Exile Log Tools", Layout,).Finalize()

while True:
	event, values = window.read()
	
	if event == "CounterClear":
		# Clear Counters
		Logging.ResetCounters()
		
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
		elif capture == True:
			Logging.stop()
			window['CaptureToggle'].update("Start Capture")		
			capture = False
		
	elif event == sg.WIN_CLOSED:
		break
	
window.close()
