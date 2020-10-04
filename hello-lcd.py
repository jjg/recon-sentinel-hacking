import time
import rslcd

if __name__ == '__main__':
    
    rslcd.lcd_init()

    while True:

        # Send some test
        rslcd.lcd_string("Hello      ", rslcd.LCD_LINE_1)
        rslcd.lcd_string("      World", rslcd.LCD_LINE_2)

        time.sleep(3)
