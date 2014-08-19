from flask import Flask
from flask import render_template, jsonify, request, make_response
from random import randint
from threading import Thread
import sys, os, time, json
working_directory = os.getcwd()
print working_directory
sys.path.append( working_directory + '/lib/python-hue' );
from hue import Hue;
global SIMULATING_MODE
SIMULATING_MODE = False

h = Hue(); # Initialize the class
h.station_ip = "192.168.1.101"  # Your base station IP
h.client_identifier = "newdeveloper"

# beacon_timestamp = 0
if SIMULATING_MODE != True:
	state = h.get_state(); # Authenticate, bootstrap your lighting system
	l = h.lights.get('l1') # get bulb #1
	l.alert() # short alert
	l.rgb(255,255,255)

app = Flask(__name__)
@app.route('/')
def index():
    # list_bulbs = {'name':'debug bulb'}
    return render_template('index.html',list_bulbs = list_bulbs, list_phones = list_phones)
@app.route('/maps')
def maps():
	return render_template('maps.html',list_bulbs = list_bulbs, list_phones = list_phones)
@app.route('/analytics')
def analytics():
	return render_template('analytics.html')
@app.route('/setting')
def setting():
	thread_status = bulb_thread.isAlive()
	print thread_status
	return render_template('setting.html',lights = h.lights, beacon_timestamp = beacon_timestamp)
@app.route('/about')
def about():
	return render_template('about.html')
#bulb commands
@app.route('/_ajax_bulb_cmd')
def _ajax_bulb_cmd():
	global beacon_thread_control 
	global beacon_interval
	cmd = request.args.get('cmd', '', type=str)
	interval = request.args.get('interval', 10, type=int)
	if cmd == "broadcasting":
		print "broadcasting"
		beacon_thread_control = 1
		beacon_interval = interval
		print beacon_interval
	elif cmd == "halt":
		print "halt"
		beacon_thread_control = 0
	elif cmd == "checking":
		print "checking"
	#	send bulb arlet cmd
	return jsonify(result="success")
#phone data
@app.route('/_LiveByte/clients', methods=['GET','POST'])
def _LiveByte_clients():
	systemtime = time.time()
	global list_phones, list_bulbs
	INIT_TIME = 0
	CHECK_BEACON = 1
	cmdtype = request.form['Type']
	devicename = request.form['Name']
	device_timestamp = request.form['TimeStamp']
	device_ssid = request.form['SSID']
	location_x = request.form['position-x']
	location_y = request.form['position-y']
	
	device_ssid = json.loads(device_ssid)
	# print device_ssid[0]['ssid_name']
	device_timestamp = long(device_timestamp)
	# print 'devicename'
	# print devicename
	print 'cmdtype'
	print cmdtype
	# print 'location-x'
	# print location_x
	# print 'location-y'
	# print location_y
	
	if int(cmdtype) == INIT_TIME:
		shift_time = systemtime*1000 - device_timestamp
		print "shift:"
		print systemtime
		print device_timestamp
		print shift_time
		print "this is shift "
		device_entity = get_device_entity_by_name(devicename)
		if device_entity == None:
			device_entity = new_device_entity(devicename)
			device_entity['status'] = 'connected'
			device_entity['location'] = 'unknown'
			device_entity['ssid'] = device_ssid
			add_device_entity(device_entity)
		else:
			device_entity['status'] = 'connected'
			device_entity['location'] = 'unknown'
			device_entity['ssid'] = device_ssid
			device_entity['shift_time'] = shift_time
			# print device_entity
			update_device_entity(device_entity)
		#update device entity
		# print list_phones
		return make_response("ok",200)
	elif int(cmdtype) == CHECK_BEACON:
		device_entity = get_device_entity_by_name(devicename)
		if device_entity == None:
			return make_response("nan",200)
		else:
			device_entity['status'] = 'connected'
			device_entity['location'] = 'l1'
			device_entity['ssid'] = device_ssid
			device_entity['position-x'] = int(location_x)
			device_entity['position-y'] = int(location_y)
			device_entity['timestamp'] = long(device_timestamp)
			# print device_entity
			update_device_entity(device_entity)
			print list_bulbs[0]['timestamp']
			print device_entity['shift_time']
			# diff = long(list_bulbs[0]['timestamp']) + long(device_entity['shift_time']) - long(device_entity['timestamp'])
			diff = systemtime - list_bulbs[0]['timestamp']
			print "diff"
			print diff
			if(diff > 0 and diff < 1):
				return make_response("ok",200)
			else:
				return make_response("nan",200)
	else:
		print 'not defined'
	return make_response("nan",200)
#bulb thread
def beacon_sending(beacon_type=1):
	# l.rgb(255, 255, 240,transitiontime=1)#240:work not fast
	# time.sleep(0.1)
	# l.rgb(255, 255, 255,transitiontime=1)
	# time.sleep(0.1)
	time.sleep(0.1)
	l.rgb(255,255,235,bri=255,transitiontime=1)
	time.sleep(0.1)
	l.rgb(255,255,255,bri=255,transitiontime=1)
	
def beacon_thread(encoding_method):
	global list_bulbs
	global beacon_thread_control
	global beacon_interval
	# beacon_timestamp = 0
	global SIMULATING_MODE
	run_flag = not SIMULATING_MODE
	while run_flag:
		if beacon_thread_control == 1:
			
			beacon_sending(beacon_type=1)
			list_bulbs[0]['timestamp'] = time.time()
			#print "running"
			#print list_bulbs[0]['timestamp']
		elif beacon_thread_control == 0:
			#print "halt"
			list_bulbs[0]['timestamp'] = 0
		#print beacon_interval
		time.sleep(1*beacon_interval)
def new_device_entity(devicename):
	new_device = {'name':devicename,'status':None,'timestamp':None,'location':None,'position-x':None,'position-y':None,'signal_type':None,'ssid':None,'shift_time':None}
	return new_device
def get_device_entity_by_name(devicename):
	global list_phones
	for phone in list_phones:
		if phone['name'] == devicename:
			return phone
	return None
def update_device_entity(entity):
	global list_phones
	for phone in list_phones:
		if phone['name'] == entity:
			phone = entity

def add_device_entity(entity):
	global list_phones
	list_phones.append(entity)
if __name__ == '__main__':
	# bulb_thread = thread.start_new_thread(bulb_thread,(1,1000))
	global bulb_thread
	global beacon_timestamp
	global beacon_thread_control 
	global list_bulbs, list_phones
	global beacon_interval
	beacon_timestamp = 0
	beacon_interval = 10
	list_bulbs = [{
		'name':'l1','status':'broadcasting','location':'landmark-01','timestamp':None,'ssid':\
			[{'ssid_name':'ssid debug 01','ssid_level':-10},{'ssid_name':'ssid debug 012','ssid_level':-10}]},]
	list_phones = []
	new_enity_phone = new_device_entity('debug-01')
	add_device_entity(new_enity_phone)
	new_enity_phone = new_device_entity('debug-03')
	add_device_entity(new_enity_phone)
	
	beacon_thread_control = 1
	beacon_interval = 3
	# h.start
	bulb_thread = Thread(target = beacon_thread, args = (1, ))
	bulb_thread.setDaemon(True)
	bulb_thread.start()
	# print thread_status
	app.run(debug = True, host = "0.0.0.0", port = 80)