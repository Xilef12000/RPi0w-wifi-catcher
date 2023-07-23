cd /home/pi

sudo apt-get update
sudo apt-get install git -y
sudo apt-get install python3-pip -y
sudo apt-get install python3-rpi.gpio -y
sudo pip install sqlite-web

git clone https://github.com/Xilef12000/RPi0w-wifi-catcher
sudo chmod a+x RPi0w-wifi-catcher/run.sh
sudo cp RPi0w-wifi-catcher/wifi-catcher.service /etc/systemd/system/wifi-catcher.service
sudo chmod 644 /etc/systemd/system/wifi-catcher.service

touch /home/pi/RPi0w-wifi-catcher/wifi.db
sudo python3 /home/pi/RPi0w-wifi-catcher/setup.py

sudo systemctl enable wifi-catcher.service
sudo reboot