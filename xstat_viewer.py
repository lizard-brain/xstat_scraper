import matplotlib.pyplot as plt
import csv



def day_viewer():
        
        with open('database.csv', mode='r', newline='') as database_csv:
                database = csv.reader(database_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for row in database:
                    
                    index = row[0]
                    #print(index)
                    video_name = row[1]
                    print(video_name)
                    
                    video_url = row[2]
                    #print(video_url)
                    #video_path = './data/' + row[0] + '_stats'
                    video_path = './data/0_stats'
                    print(video_path)
                    x = []
                    y = []
                with open(video_path, mode='r', newline='') as video_path_csv:
                        video_data = csv.reader(video_path_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        for row in video_data:
                                print(row)
                                x.append(row[1])
                                y.append(row[2])
                               
        plt.plot(x,y)
        plt.show()
        

day_viewer()
