import RPi.GPIO as GPIO
import iwlist
import sqlite3
from time import time
from datetime import datetime
import board
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import os

i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
oled.fill(0)
oled.show()
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)
#font = ImageFont.load_default()
font = ImageFont.truetype(font="DejaVuSans", size=14)

con = sqlite3.connect("/home/pi/RPi0w-wifi-catcher/wifi.db")
cur = con.cursor()

LED_R = 13
LED_G = 19
LED_B = 26
BUT_E = 21
BUT_U = 22
BUT_D = 17
BUT_L = 27
BUT_R = 6

def butEn(but = 0):
	global txtIp
	txtIp = os.popen("ip a | grep wlan0 | grep inet | awk  '{print $2}'").read().split('\n')[0]
	global timeOnLast
	timeOnLast = time()
	global powerStateOn
	powerStateOn = True
	colorRefresh()
	oled.poweron()
	timeHold = time()
	while GPIO.input(but) == GPIO.LOW:
		if timeHold + timeHoldOff/2 < time():
			setStatus("poweroff?", "V")
		if timeHold + timeHoldOff < time():
			setStatus("poweroff...", "R")
			global brex
			brex = True
			
def butPr(but = 0):
	global powerStateOn
	global timeWait
	global timeOnLast
	if powerStateOn:
		timeOnLast = time()
		if but == BUT_L and timeWait > 0:
			timeWait -= 1
		elif but == BUT_R and timeWait < 10:
			timeWait += 1
		oledRefresh()

#GPIO.setwarnings(False)
#GPIO.setmode(GPIO.BCM)
GPIO.setup(BUT_E, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUT_U, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUT_D, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUT_L, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUT_R, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(BUT_E,GPIO.FALLING,callback=butEn)
GPIO.add_event_detect(BUT_L,GPIO.FALLING,callback=butPr)
GPIO.add_event_detect(BUT_R,GPIO.FALLING,callback=butPr)
GPIO.setup(LED_R, GPIO.OUT)
GPIO.setup(LED_G, GPIO.OUT)
GPIO.setup(LED_B, GPIO.OUT)

timeHoldOff = 5
timeWait = 5
timeOn = 10
timeOnLast = time()
powerStateOn = True
txtSetStatus = "test"
txtCount = 0
txtCountNow = 0
txtIp = os.popen("ip a | grep wlan0 | grep inet | awk  '{print $2}'").read().split('\n')[0]
ledColor = ""
brex = False
def oledRefresh():
	draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)
	(font_width, font_height) = font.getsize("txt")
	draw.text(
	    (0, 0),
	    str(txtCount),
	    font=font,
	    fill=255,
	)
	draw.text(
	    (oled.width // 2, 0),
	    str(txtCountNow),
	    font=font,
	    fill=255,
	)
	draw.text(
	    (0, font_height),
	    txtSetStatus,
	    font=font,
	    fill=255,
	)
	draw.text(
	    (0, font_height*2),
	    txtIp,
	    font=font,
	    fill=255,
	)
	draw.text(
	    (0, font_height*3),
	    str(timeWait),
	    font=font,
	    fill=255,
	)
	oled.image(image)
	oled.show()
def setStatus(txt = "", col = ""):
	global txtSetStatus
	txtSetStatus = txt
	global ledColor
	ledColor = col
	if powerStateOn:
		oledRefresh()
		colorRefresh()
def colorRefresh():
	global ledColor
	GPIO.output(LED_R, GPIO.LOW)
	GPIO.output(LED_G, GPIO.LOW)
	GPIO.output(LED_B, GPIO.LOW)
	if(ledColor=="R"):
		GPIO.output(LED_R, GPIO.HIGH)
	elif(ledColor=="G"):
		GPIO.output(LED_G, GPIO.HIGH)
	elif(ledColor=="B"):
		GPIO.output(LED_B, GPIO.HIGH)
	elif(ledColor=="Y"):
		GPIO.output(LED_R, GPIO.HIGH)
		GPIO.output(LED_G, GPIO.HIGH)
	elif(ledColor=="V"):
		GPIO.output(LED_R, GPIO.HIGH)
		GPIO.output(LED_B, GPIO.HIGH)
	elif(ledColor=="T"):
		GPIO.output(LED_G, GPIO.HIGH)
		GPIO.output(LED_B, GPIO.HIGH)		
colorRefresh()
while True:
	timeEnd = time() + timeWait
	if timeOnLast + timeOn < time():
		oled.poweroff()
		ledColor = ""
		colorRefresh()
		powerStateOn = False
	setStatus("scanning...", "G")
	content = iwlist.scan(interface="wlan0")
	timeNow = time()
	setStatus("parsing...", "Y")
	cells = iwlist.parse(content)
	#print(datetime.utcfromtimestamp(timeNow).strftime('%Y-%m-%d %H:%M:%S'))
	txtCountNow = len(cells)
	for cell in cells:
		#print(cell["mac"], cell["essid"], int(cell["channel"]), cell["encryption"])
		with con:
			con.execute("INSERT OR REPLACE INTO WIFI VALUES (?, ?, ?, ?, ?)", (cell["mac"], cell["essid"], int(cell["channel"]), cell["encryption"], timeNow))
	with con:
		cur.execute("SELECT COUNT (*) FROM WIFI")
	txtCount = cur.fetchall()[0][0]
	setStatus("waiting...", "B")
	br = False
	while time() < timeEnd:
		if brex:
			con.close()
			ledColor = ""
			colorRefresh()
			oled.poweroff()
			exit()