import shutil
import rslcd

if __name__ == '__main__':
    
    rslcd.lcd_init()

    # Get disk info
    total, used, free = shutil.disk_usage("/storage")
    free_gb = f"{(free // (2**30))} GiB"

    # Send some test
    rslcd.lcd_string("Disk Free: ", rslcd.LCD_LINE_1)
    rslcd.lcd_string(free_gb, rslcd.LCD_LINE_2)
