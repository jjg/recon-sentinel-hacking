# i2c stuff taken from https://shiroku.net/robotics/using-i2c-lcd-on-raspberry-pi/

import time
import csv
import urllib.request

import smbus2 as smbus

# Define some device parameters
I2C_ADDR = 0x3f     # I2C device address, if any error, change this address to 0x3f
LCD_WIDTH = 16      # Maximum characters per line

# Define some device constants
LCD_CHR = 1     # Mode - Sending data
LCD_CMD = 0     # Mode - Sending command

LCD_LINE_1 = 0x80   # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0   # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94   # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4   # LCD RAM address for the 4th line

LCD_BACKLIGHT = 0x08  # On

ENABLE = 0b00000100     # Enable bit

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

# Open I2C interface
# bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
bus = smbus.SMBus(1)    # Rev 2 Pi uses 1


def lcd_init():
    # Initialise display
    lcd_byte(0x33, LCD_CMD)     # 110011 Initialise
    lcd_byte(0x32, LCD_CMD)     # 110010 Initialise
    lcd_byte(0x06, LCD_CMD)     # 000110 Cursor move direction
    lcd_byte(0x0C, LCD_CMD)     # 001100 Display On,Cursor Off, Blink Off
    lcd_byte(0x28, LCD_CMD)     # 101000 Data length, number of lines, font size
    lcd_byte(0x01, LCD_CMD)     # 000001 Clear display
    time.sleep(E_DELAY)


def lcd_byte(bits, mode):
    # Send byte to data pins
    # bits = the data
    # mode = 1 for data
    #        0 for command

    bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
    bits_low = mode | ((bits << 4) & 0xF0) | LCD_BACKLIGHT

    # High bits
    bus.write_byte(I2C_ADDR, bits_high)
    lcd_toggle_enable(bits_high)

    # Low bits
    bus.write_byte(I2C_ADDR, bits_low)
    lcd_toggle_enable(bits_low)


def lcd_toggle_enable(bits):
    # Toggle enable
    time.sleep(E_DELAY)
    bus.write_byte(I2C_ADDR, (bits | ENABLE))
    time.sleep(E_PULSE)
    bus.write_byte(I2C_ADDR, (bits & ~ENABLE))
    time.sleep(E_DELAY)


def lcd_string(message, line):
    # Send string to display
    message = message.ljust(LCD_WIDTH, " ")

    lcd_byte(line, LCD_CMD)

    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]), LCD_CHR)


if __name__ == '__main__':



    # Get the county-level data from DHS?
    url = "https://opendata.arcgis.com/datasets/b913e9591eae4912b33dc5b4e88646c5_10.csv?where=GEO%20%3D%20%27County%27&outSR=%7B%22latestWkid%22%3A3857%2C%22wkid%22%3A102100%7D"

    response = urllib.request.urlopen(url)
    lines = [l.decode("utf-8") for l in response.readlines()]
    county_rows = csv.DictReader(lines)

    # Extract only the rows for the county we're interested in
    selected_county_rows = []
    for row in county_rows:
        if row["NAME"] == "Dodge":
            selected_county_rows.append(row)

    # Sort the rows so the most recent is at the top
    selected_county_rows.sort(key=lambda x: x["DATE"], reverse=True)

    # Grab the most recent day's new positive count
    pos_new = int(selected_county_rows[0]["POS_NEW"])

    # Compute the 7-day average new positives
    last_seven_total = 0
    for i in range(0,7):
        #print(selected_county_rows[i]["POS_NEW"])
        last_seven_total += int(selected_county_rows[i]["POS_NEW"])

    pos_new_seven_day_avg = last_seven_total / 7

    # Compute the new positives per 100k
    county_population = 90005
    pos_new_per_100k = (pos_new_seven_day_avg / county_population) * 100000

    line_1 = f"New Positive: {pos_new}"
    line_2 = f"{round(pos_new_per_100k,2)}% per 100k"

    # DEBUG
    print(line_1)
    print(line_2)

    lcd_init()

    lcd_string(line_1, LCD_LINE_1)
    lcd_string(line_2, LCD_LINE_2)

#    while True:
#        # Send some test
#        lcd_string("Hello      ", LCD_LINE_1)
#        lcd_string("      World", LCD_LINE_2)
#
#        time.sleep(3)
