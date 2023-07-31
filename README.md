# RPi0w-wifi-catcher
A Raspberry Pi Zero W based wifi scanner

**This Project is currently under development**
## Setup:
### Button:
*using a simple push-button with pull-up resistor*

| button | pi0w  | PIN |
|--------|-------|-----|
| GND    | GND   | 6   |
| VIN    | 3V3   | 2   |
| Signal | GPIO4 | 7   |

### RGB-LED:
*using a common-cathode RGB-LED*

| LED   | pi0w   | PIN |
|-------|--------|-----|
| GND   | GND    | 39  |
| red   | GPIO26 | 37  |
| green | GPIO21 | 40  |
| blue  | GPIO20 | 38  |

### 0.96" I2C OLED Display::
| OLED | pi0w        | PIN |
|------|-------------|-----|
| GND  | GND         | 9   |
| VCC  | 3V3         | 1   |
| SCL  | GPIO3/SCL   | 5   |
| SDA  | GPIO2/SDA   | 3   |

### boot preparation:
1. flash SD-Card with Raspberry Pi OS light (configure your wifi now!)

for more information see [this article by the Raspberry Pi Spy](https://www.raspberrypi-spy.co.uk/2020/05/adding-ethernet-to-a-pi-zero/)

## Installation:
```
wget https://raw.githubusercontent.com/Xilef12000/RPi0w-wifi-catcher/main/setup.sh
sudo chmod a+x setup.sh
sudo sh setup.sh
```

open the webpage on port 8080

a long button-press will turn your pi off