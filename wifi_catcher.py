import RPi.GPIO as GPIO
import iwlist
import sqlite3
from time import time
from datetime import datetime

con = sqlite3.connect("/home/pi/RPi0w-wifi-catcher/wifi.db")
cur = con.cursor()

LED_PIN_R = 37
LED_PIN_G = 40
LED_PIN_B = 38

BUTTON_PIN = 7

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(BUTTON_PIN, GPIO.IN)
GPIO.setup(LED_PIN_R, GPIO.OUT)
GPIO.setup(LED_PIN_G, GPIO.OUT)
GPIO.setup(LED_PIN_B, GPIO.OUT)

def color(col = ""):
	GPIO.output(LED_PIN_R, GPIO.LOW)
	GPIO.output(LED_PIN_G, GPIO.LOW)
	GPIO.output(LED_PIN_B, GPIO.LOW)
	if(col=="R"):
		GPIO.output(LED_PIN_R, GPIO.HIGH)
	elif(col=="G"):
		GPIO.output(LED_PIN_G, GPIO.HIGH)
	elif(col=="B"):
		GPIO.output(LED_PIN_B, GPIO.HIGH)
	elif(col=="Y"):
		GPIO.output(LED_PIN_R, GPIO.HIGH)
		GPIO.output(LED_PIN_G, GPIO.HIGH)
	elif(col=="V"):
		GPIO.output(LED_PIN_R, GPIO.HIGH)
		GPIO.output(LED_PIN_B, GPIO.HIGH)
	elif(col=="T"):
		GPIO.output(LED_PIN_G, GPIO.HIGH)
		GPIO.output(LED_PIN_B, GPIO.HIGH)

			
color()
while True:
	color("G")
	content = iwlist.scan(interface="wlan0")
	timeNow = time()
	color("Y")
	cells = iwlist.parse(content)
	#print(datetime.utcfromtimestamp(timeNow).strftime('%Y-%m-%d %H:%M:%S'))
	for cell in cells:
		#print(cell["mac"], cell["essid"], int(cell["channel"]), cell["encryption"])
		with con:
			con.execute("INSERT OR REPLACE INTO WIFI VALUES (?, ?, ?, ?, ?)", (cell["mac"], cell["essid"], int(cell["channel"]), cell["encryption"], timeNow))
	color("B")
	br = False
	timeEnd = time() + 5
	while time() < timeEnd:
		if GPIO.input(BUTTON_PIN) == GPIO.LOW:
			color("R")
			timeButtonEnd = time() + 3
			while GPIO.input(BUTTON_PIN) == GPIO.LOW:
				if time() > timeButtonEnd:
					br = True
					break
			if not br:
				color("B")
		if br:
			break
	if br:
		break
color()
con.close()