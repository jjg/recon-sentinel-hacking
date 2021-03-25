import rslcd
import subprocess

if __name__ == '__main__':


    result = subprocess.run(["wg", "show", "wg1", "transfer"], stdout=subprocess.PIPE)
    result_string = result.stdout.decode("utf-8")
    result_array = result_string.split("\n")[0].split("\t")
    throughput_k = (float(result_array[1]) + float(result_array[2]))/1024

    line_1 = "TheTubes"
    line_2 = f"{throughput_k:.1f}k bytes"

    # DEBUG
    print(line_1)
    print(line_2)

    rslcd.lcd_init()

    rslcd.lcd_string(line_1, rslcd.LCD_LINE_1)
    rslcd.lcd_string(line_2, rslcd.LCD_LINE_2)
