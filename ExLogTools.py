#
#
#

import PySimpleGUI as sg
import ctypes
import platform
from main import ExiLogger

def make_dpi_aware():
	# Fix blurry text on high dpi monitors
	# reqs: ctypes, platform
	# https://github.com/PySimpleGUI/PySimpleGUI/issues/1179
    if int(platform.release()) >= 8:
        ctypes.windll.shcore.SetProcessDpiAwareness(True)
        
OutVals = ""
logThread = ""
Logging = 0
        
Layout = [
		[sg.Text("Log File:"),sg.Input(size=(80,0),key="LogPath"),sg.FileBrowse(file_types=(("Log Files","*.log"),))],
		[sg.Button("Start Capture",key="CaptureStart"),sg.Button("Stop Capture",key="CaptureStop"),sg.Text("  "),sg.Button("Clear Counters",key="CounterClear"),sg.Button("Clear Window",key="WindowClear")],
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
		
	elif event == "CaptureStop":
		# Stop capturing logs
		#capture_stop(logThread,xEvent)
		Logging.stop()
		
	elif event == "CaptureStart":
		# Start capturing logs
		#print("Values: ")
		#print(repr(values))
		
		Logging = ExiLogger()
		Logging.start(window,values['LogPath'],True)
		#print("LogPath  : {0}".format(values['LogPath']))
		#logThread, xEvent = capture_start(window,values['LogPath'],True)
		#toggle_xEvent("start",xEvent)
		
	elif event == sg.WIN_CLOSED:
		break
	
window.close()
