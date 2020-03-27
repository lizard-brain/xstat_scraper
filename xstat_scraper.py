'''
Logs the views over time UTC Time

0.8 Changed to read from index

0.9 Logfiles changed to index numbers, swaped epoch time and view counts now: (24hr time, epoch, view cout)


'''
#------------------------------------------------------------------------------------------------------

import time
import csv
import re
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#------------------------------------------------------------------------------------------------------

#Start Browser

options = FirefoxOptions()
#options.add_argument("--headless")
print("Starting Firefox...")
browser = Firefox(options=options, executable_path='/home/jace/Documents/Reddit_bot/geckodriver')
print("Started",'\n')

#------------------------------------------------------------------------------------------------------

#Go to Url

def goto(url):

    print("Loading Page...")
    browser.get(url)
    print("Loaded", '\n')
    
#------------------------------------------------------------------------------------------------------
    
#Catagory List Scrapper
    
def cat_scraper():

    print('Seaching Catagories...', '\n')
    cat_list = []
    scraper = browser.find_elements_by_xpath("//a[contains(@href,'/search/video')]")
    for scraper in scraper:
        cat = scraper.get_attribute("href")
        cat = cat[35:]
        cat_list.append(cat)
        print(cat)   
    #print('Categories:', cat_list, '\n')
    print('')
    return cat_list

#------------------------------------------------------------------------------------------------------

def tag_scraper():

    '''Notes
    Really hacky way to find the tags
    Gave up using xpath to search the child of 'tagcatagories'
    Revisit if it 
    '''
    print('Seaching Tags...','\n')
    tag_list = []
    scraper = browser.find_elements_by_xpath("//a[contains(@href,'/video')]")
    i = 0
    for scraper in scraper:
        tag = scraper.get_attribute("href")
        tag = tag[28:]
        tag_list.append(tag)
        print(tag)
        
        i += 1
        if i == 3:
            break
    print('')
    return tag_list

#------------------------------------------------------------------------------------------------------

def view_scraper():

    print('Collecting Views...')
    #cat_list = []
    for elem in browser.find_elements_by_xpath('.//span[@class = "viewsCount"]'):
        views = elem.text
        views = views.split(" ")[0]
        views = int(views)
        print('Views: ',views,'\n')
        return views

#------------------------------------------------------------------------------------------------------
        
def like_scraper():

    print('Collecting Votes...')
    #cat_list = []
    for elem in browser.find_elements_by_xpath('//div[@class="votesWrapper"]/*'):
        views = elem.text
        print(views,'\n')
        like_pct = views.split("%")[0]
        print(like_pct)

#------------------------------------------------------------------------------------------------------

def view_log():

    
    with open('database.csv', mode='r', newline='') as database_csv:
    
        database = csv.reader(database_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in database:
            video_path = './data/' + row[0] + '_stats' 
            video_name = row[1]
            print(video_name)
            #print(video_path)
            video_url = row[2]
            print(video_url)

            with open(video_path, mode='a', newline='') as video_csv: #a for append
                csv_file = csv.writer(video_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                goto(video_url)
                views = view_scraper()
                csv_file.writerow([time.strftime('%H:%M', time.localtime()), time.time(), views ])

                


#------------------------------------------------------------------------------------------------------
i = 1
while i > 0:
    cycle_start = time.time()
    view_log()
    cycle_end = time.time()
    cycle_time = cycle_end - cycle_start
    print('Cycle Time(s):', cycle_time)
    print('cycle complete', time.strftime('%H:%M', time.localtime())
    goto('https://duckduckgo.com')
    time.sleep(1800) #30mins wait before  refresh
    print('Waiting 30mins')
    

    



    
    
    






