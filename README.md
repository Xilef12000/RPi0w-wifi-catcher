# RPi0w-wifi-catcher
A Raspberry Pi Zero W based wifi scanner

**This Project is currently under development**
## Setup:
### Button:
*using a simple push-button with pull-up resistor*

| buttons | GPIO |
|---------|------|
| GND     | GND  |
| enter   | 21   |
| up      | 22   |
| down    | 17   |
| left    | 27   |
| right   | 6    |

### RGB-LED:
*using a common-cathode RGB-LED*

| LED   | GPIO |
|-------|------|
| GND   | GND  |
| red   | 13   |
| green | 19   |
| blue  | 26   |

### 0.96" I2C OLED Display::
| OLED | GPIO  |
|------|-------|
| GND  | GND   |
| VCC  | 3V3   |
| SCL  | 3 SCL |
| SDA  | 2 SDA |

### boot preparation:
1. flash SD-Card with Raspberry Pi OS light (configure your wifi now!)

for more information see [this article by the Raspberry Pi Spy](https://www.raspberrypi-spy.co.uk/2020/05/adding-ethernet-to-a-pi-zero/)

## Installation:
```
wget https://raw.githubusercontent.com/Xilef12000/RPi0w-wifi-catcher/main/setup.sh
sudo chmod a+x setup.sh
sudo sh setup.sh
```

open the webpage on `http://YOURPI'SIP:8080/wifi/content/`

short Enter press: turn display on
long Enter press: turn pi off
short left/right press while display is on: decrease/increase delay between scanning
