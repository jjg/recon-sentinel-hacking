# Journal

## 10022020

Pulled the case apart and loaded the SD card with Armbian.  Need to disconnect the LCD in order to connect a console cable.

Console connects to pins 6 (gnd), 8 (tx) and 10 (rx).

`picocom -b 1500000 /dev/ttyUSB0`

This works, but with no ethernet attached you can't do much more than set the passwords.

LCD pin-out:

| Wire | ROCK64 Pin | LCD Module Pin |
|------|------------|----------------|
| red | 2/5v | VCC |
| grey | 6/gnd | GND
| brown | 28/GPIO2_A5/I2C1_SCL | SCL |
| blue | 27/GPIO2_A4/I2C1_SDA | SDA |

Changed hostname to rock1.local

Let's try talking to the LCD

`sudo apt install i2c-tools`
`sudo i2cdetect -y 1`

```
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- UU -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 3f
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: -- -- -- -- -- -- -- --
```

Python 3 is installed, but not much of it, and we need more to do anything useful so...

`sudo apt install python3-pip`
`sudo apt install python3-venv`

Now create a venv so we can keep track of dependencies

`python3 -m venv ./venvs/hello-lcd`
`source ./venvs/hello-lcd/bin/activate`
`pip install wheel`

Now install the i2c stuff we need

`pip install smbus2`

OK, now run the hello-lcd.py script as root.

`sudo ~/venvs/hello-lcd/bin/python ./hello-lcd.py`

Experimented with using some code from the covid repo and ran into a little problem installing dependencies.  This was needed:

`sudo apt install python3-dev`



### References

* `http://files.pine64.org/doc/rock64/ROCK64_Pi-2%20_and_Pi_P5+_Bus.pdf`
* `https://www.armbian.com/rock64/`
* `https://forum.pine64.org/showthread.php?tid=5902`
* `https://shiroku.net/robotics/using-i2c-lcd-on-raspberry-pi/`


## 10032020

Trying to build pandas causes me to loose connection with the board.  It's not clear why, or if the board crashes/resets of if it's just the network that drops, but I'm going to give it one more try and if that doesn't work I might just re-write the script so it doesn't depend on pandas.

Refactored [covid-lcd.py](./covid-lcd.py) to eliminate the pandas dependency and now it works as expected.  Update the requirements.txt so it can be safely setup and run on the Rock w/o blowing it up.


## 10232020

Installed Plex from armbian-config and it worked surprisingly well with little effort other than mounting an NFS share where I have some movie files.

I used this guide to setup NFS and today I'm going to see if it will automount on boot.  I would assume so, but I've had trouble with this recently on Ubuntu so hopefully it's not the same deal with Debian 10.

https://linuxhint.com/mount_nfs_share_debian/

No luck.  Need to tshoot

Weirdly running `sudo mount -a` mounts the NFS share, but for some reason it didn't do it at boot.


