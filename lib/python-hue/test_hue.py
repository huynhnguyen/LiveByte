import sys, time
sys.path.append( '/Users/huynh/Desktop/livebyte_webserver/lib/python-hue' );
from hue import Hue;
h = Hue(); # Initialize the class
h.station_ip = "192.168.1.101"  # Your base station IP
h.client_identifier = "newdeveloper"
# h.authenticate
state = h.get_state(); # Authenticate, bootstrap your lighting system
li = h.lights
for key, element in li.items():
	print key, element

l = h.lights.get('l1') # get bulb #1
while 1:
	ts = time.time()
	print ts
# l.alert() # short alert
# time.sleep(0.1)
# l.alert() # short alert
# time.sleep(0.1)
# l.set_state({"bri": 220, "alert": "select","transitiontime":1}) # Complex send
# time.sleep(0.1)
# l.alert() # short alert
# time.sleep(0.1)
# l.alert() # short alert
	# l.set_state({"bri": 230, "xy":[0.3,0.322],"sat":255}) # Complex send
	# l.set_state({"bri": 230, "xy":[0.3,0.322],"sat":255}) # Complex send
	l.rgb(255, 255, 240,transitiontime=1)
	time.sleep(0.1)
	l.rgb(255,255,255,transitiontime=1)
	# l.set_state({"bri": 255, "xy":[0.3,0.322],"sat":255}) # Complex send
	time.sleep(0.1)
	time.sleep(0.8)
	ts2 = time.time()
	print ts2

