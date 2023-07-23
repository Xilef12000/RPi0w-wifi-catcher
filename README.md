# RPi0w-wifi-catcher
A Raspberry Pi Zero W based wifi scanner

**This Project is currently under development**
## Setup:
### Button:
*using a simple push-button with pull-up resistor*

| button | pi0w  | PIN |
|--------|-------|-----|
| GND    | GND   | 6   |
| VIN    | 3V3   | 1   |
| Signal | GPIO4 | 7   |

### RGB-LED:
*using a common-cathode RGB-LED*

| LED   | pi0w   | PIN |
|-------|--------|-----|
| GND   | GND    | 39  |
| red   | GPIO26 | 37  |
| green | GPIO21 | 40  |
| blue  | GPIO20 | 38  |

### ENC28J60:
| Module | pi0w        | PIN |
|--------|-------------|-----|
| CLKOUT |             |     |
| INT    | GPIO25      | 22  |
| WOL    |             |     |
| SO     | GPIO9/MISO  | 21  |
| SI     | GPIO10/MOSI | 19  |
| SCK    | GPIO11/SCLK | 23  |
| CS     | GPIO8/CE0_N | 24  |
| RESET  |             |     |
| VCC    | 3V3         | 17  |
| GND    | GND         | 14  |

### boot preparation:
1. flash SD-Card with Raspberry Pi OS light (do not configure wifi)
3. open `config.txt` of the boot partition of the SD-Card
4. add the following to the end of the file:  
```
dtparam=spi=on
dtoverlay=enc28j60
```

for more information see [this article by the Raspberry Pi Spy](https://www.raspberrypi-spy.co.uk/2020/05/adding-ethernet-to-a-pi-zero/)

## Installation:
```
wget https://raw.githubusercontent.com/Xilef12000/RPi0w-wifi-catcher/main/setup.sh
sudo chmod a+x setup.sh
sudo sh setup.sh
```

open the webpage on port 8080

a long button-press will turn your pi off