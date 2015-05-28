import csv

def replace(self, inname, outname):
    reader = csv.reader(open(inname, encoding="utf-8"))
    # writer = csv.writer(open('/Users/koitaroh/Documents/GitHub/GeoTweetCollector/data/tweet_table_20150317140247.csv', 'w', newline='', encoding="utf-8"))
    writer = csv.writer(open(outname, 'w', newline='', encoding="utf-8"))
    for row in reader:
        writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9].replace(',', ' '), row[10].replace(',', ' '), row[11].replace(',', ' '), row[12].replace(',', ' ')])