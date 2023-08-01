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

LED_PIN_R = 13
LED_PIN_G = 19
LED_PIN_B = 26

BUTTON_PIN = 21

#GPIO.setwarnings(False)
#GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LED_PIN_R, GPIO.OUT)
GPIO.setup(LED_PIN_G, GPIO.OUT)
GPIO.setup(LED_PIN_B, GPIO.OUT)


txt_action = "test"
txt_count = 0
txt_count_now = 0
def text():
	draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)
	(font_width, font_height) = font.getsize("txt")
	draw.text(
	    (0, 0),
	    str(txt_count),
	    font=font,
	    fill=255,
	)
	draw.text(
	    (oled.width // 2, 0),
	    str(txt_count_now),
	    font=font,
	    fill=255,
	)
	draw.text(
	    (0, font_height),
	    txt_action,
	    font=font,
	    fill=255,
	)
	oled.image(image)
	oled.show()

def action(txt = "", col = ""):
	global txt_action
	txt_action = txt
	text()
	color(col)
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
	with con:
		cur.execute("SELECT * FROM WIFI")
	txt_count = len(cur.fetchall())
	action("scanning...", "G")
	content = iwlist.scan(interface="wlan0")
	timeNow = time()
	action("parsing...", "Y")
	cells = iwlist.parse(content)
	#print(datetime.utcfromtimestamp(timeNow).strftime('%Y-%m-%d %H:%M:%S'))
	txt_count_now = len(cells)
	for cell in cells:
		#print(cell["mac"], cell["essid"], int(cell["channel"]), cell["encryption"])
		with con:
			con.execute("INSERT OR REPLACE INTO WIFI VALUES (?, ?, ?, ?, ?)", (cell["mac"], cell["essid"], int(cell["channel"]), cell["encryption"], timeNow))
	action("waiting...", "B")
	br = False
	timeEnd = time() + 5
	while time() < timeEnd:
		if GPIO.input(BUTTON_PIN) == GPIO.LOW:
			action("button...", "R")
			timeButtonEnd = time() + 3
			while GPIO.input(BUTTON_PIN) == GPIO.LOW:
				if time() > timeButtonEnd:
					br = True
					break
			if not br:
				action("waiting...", "B")
		if br:
			break
	if br:
		break
setStatus("exiting...", "V")
color("V")
con.close()