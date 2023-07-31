import RPi.GPIO as GPIO
import iwlist
import sqlite3
from time import time
from datetime import datetime
import board
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
oled.fill(0)
oled.show()
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

con = sqlite3.connect("/home/pi/RPi0w-wifi-catcher/wifi.db")
cur = con.cursor()

LED_PIN_R = 26
LED_PIN_G = 21
LED_PIN_B = 20

BUTTON_PIN = 4

#GPIO.setwarnings(False)
#GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN)
GPIO.setup(LED_PIN_R, GPIO.OUT)
GPIO.setup(LED_PIN_G, GPIO.OUT)
GPIO.setup(LED_PIN_B, GPIO.OUT)

def text(txt = ""):
	draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)
	(font_width, font_height) = font.getsize(txt)
	draw.text(
	    (oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2),
	    txt,
	    font=font,
	    fill=255,
	)
	oled.image(image)
	oled.show()

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
	text("scanning...")
	color("G")
	content = iwlist.scan(interface="wlan0")
	timeNow = time()
	text("parsing...")
	color("Y")
	cells = iwlist.parse(content)
	#print(datetime.utcfromtimestamp(timeNow).strftime('%Y-%m-%d %H:%M:%S'))
	for cell in cells:
		#print(cell["mac"], cell["essid"], int(cell["channel"]), cell["encryption"])
		with con:
			con.execute("INSERT OR REPLACE INTO WIFI VALUES (?, ?, ?, ?, ?)", (cell["mac"], cell["essid"], int(cell["channel"]), cell["encryption"], timeNow))
	text("waiting...")
	color("B")
	br = False
	timeEnd = time() + 5
	while time() < timeEnd:
		if GPIO.input(BUTTON_PIN) == GPIO.LOW:
			text("button...")
			color("R")
			timeButtonEnd = time() + 3
			while GPIO.input(BUTTON_PIN) == GPIO.LOW:
				if time() > timeButtonEnd:
					br = True
					break
			if not br:
				text("waiting...")
				color("B")
		if br:
			break
	if br:
		break
text("exiting...")
color("V")
con.close()