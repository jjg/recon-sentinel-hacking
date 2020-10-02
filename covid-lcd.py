#!/usr/bin/python3

# Taken from https://shiroku.net/robotics/using-i2c-lcd-on-raspberry-pi/

import smbus2 as smbus
import time
import pandas as pd

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


# COVID stuff
def download_data():
    q = "https://opendata.arcgis.com/datasets/b913e9591eae4912b33dc5b4e88646c5_10.csv?where=GEO%20%3D%20%27County%27&outSR=%7B%22latestWkid%22%3A3857%2C%22wkid%22%3A102100%7D"
    return pd.read_csv(q)

def process_data(ds):
    county = "Dodge"
    county_population = 90005

    dc = ds[ds.NAME == county]

    dc_summary = dc[["DATE", "NEGATIVE", "POSITIVE", "DEATHS", "DTH_NEW", "HOSP_YES", "POS_NEW"]].sort_values(["DATE"], ascending=False).head(20)

    # Reverse the sort
    dc_summary = dc_summary.sort_values(["DATE"], ascending=True)

    dc_summary["rolling_positive"] = (dc_summary["POSITIVE"]/(dc_summary["POSITIVE"] + dc_summary["NEGATIVE"])) * 100

    # Add a calculated column for the "new cases per 100k of population" from the Harvard model
    dc_summary["pos_new_rolling"] = dc_summary["POS_NEW"].rolling(7).mean()
    dc_summary["new_per_100k"] = (dc_summary["pos_new_rolling"] / county_population) * 100000

    # Grab last week and sort
    dc_summary = dc_summary.tail(7).sort_values(["DATE"], ascending=False)

    return dc_summary



if __name__ == '__main__':
    lcd_init()

    ds = download_data()

    summary = process_data(ds)
    line_1 = f"New: {summary.iloc[0]['POS_NEW']}"
    line_2 = f"{summary.iloc[0]['new_per_100k']}% new per 100k"

    lcd_string(line_1, LCD_LINE_1)
    lcd_string(line_2, LCD_LINE_2)

#    while True:
#        # Send some test
#        lcd_string("Hello      ", LCD_LINE_1)
#        lcd_string("      World", LCD_LINE_2)
#
#        time.sleep(3)
