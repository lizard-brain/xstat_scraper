import matplotlib.pyplot as plt
import csv


def day_viewer():
        
        with open('database.csv', mode='r', newline='') as database_csv:
                database = csv.reader(database_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for row in database:
                    video_path = './data/' + row[0] + '_stats'
                    index = row[0]
                    print(index)
                    video_name = row[1]
                    print(video_name)
                    #print(video_path)
                    video_url = row[2]
                    print(video_url)

day_viewer()
