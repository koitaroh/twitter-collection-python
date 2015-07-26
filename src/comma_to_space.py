import csv

def replace(inname, outname):
    reader = csv.reader(open(inname, encoding="utf-8"))
    # reader = csv.reader((line.replace('\0','') for line in inname), delimiter=",")
    # writer = csv.writer(open('/Users/koitaroh/Documents/GitHub/GeoTweetCollector/data/tweet_table_20150317140247.csv', 'w', newline='', encoding="utf-8"))
    writer = csv.writer(open(outname, 'w', newline='', encoding="utf-8"))
    for row in reader:
        for x in row:
            x.replace('\0', '')
            x.replace('\x00', '')
            x.replace('\\', '')
        # reader = csv.reader(x.replace('\0', '') for x in mycsv)
        # data = csv.reader((line.replace('\0','') for line in inname), delimiter=",")
        writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9].replace(',', ' '), row[10].replace(',', ' '), row[11].replace(',', ' '), row[12].replace(',', ' ')])

if __name__ == '__main__':
    inname = '/Users/koitaroh/Documents/GitHub/GeoTweetCollector/data/tweet_table_20150317142835_5.csv'
    outname = '/Users/koitaroh/Documents/GitHub/GeoTweetCollector/data/tweet_table_20150317142835_space.csv'
    replace(inname, outname)


