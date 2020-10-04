import csv
import urllib.request
import rslcd

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

    rslcd.lcd_init()

    rslcd.lcd_string(line_1, rslcd.LCD_LINE_1)
    rslcd.lcd_string(line_2, rslcd.LCD_LINE_2)
