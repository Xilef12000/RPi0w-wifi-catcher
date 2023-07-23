import sqlite3

con = sqlite3.connect("/home/pi/RPi0w-wifi-catcher/wifi.db")
cur = con.cursor()
with con:
	con.execute("DROP TABLE IF EXISTS WIFI")
	con.execute('''CREATE TABLE wifi(
					mac varchar(17),
					essid varchar(32) NOT NULL,
					channel tinyint,
					encryption varchar(8),
					last_seen INTEGER(11),
					PRIMARY KEY (mac)
				)''')
con.close()