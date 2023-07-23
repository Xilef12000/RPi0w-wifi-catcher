sudo apt-get update
sudo apt-get install git -y
sudo apt-get install python3-pip -y
sudo apt-get install python3-rpi.gpio -y
pip install sqlite-web

git clone https://github.com/Xilef12000/RPi0w-wifi-catcher
sudo chmod a+x RPi0w-wifi-catcher/run.sh
cp RPi0w-wifi-catcher/wifi-catcher.service /etc/systemd/system/wifi-catcher.service
chmod 644 /etc/systemd/system/wifi-catcher.service
systemctl enable wifi-catcher.service