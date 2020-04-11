'''
added feature to only update csv when views have changed by a certain amount

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
browser = Firefox(options=options, executable_path='./geckodriver') # need to add directory to path
print("Started",'\n')

#------------------------------------------------------------------------------------------------------

#Go to Url

def goto(url):

    print("Loading Page:", url)
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


# Setup a view list the size of how many videos are in database this is for the view_log function
# the first run of the script will record data
view_lst = []

with open('database.csv', mode='r', newline='') as database_csv:
    database = csv.reader(database_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for row in database:
        view_lst.append(1)

        
def view_log():

    
    with open('database.csv', mode='r', newline='') as database_csv:
    
        database = csv.reader(database_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in database:
            index = int(row[0])
            #print(index)
            video_path = './data/' + row[0] + '_stats' 
            video_name = row[1]
            print(video_name)
            video_url = row[2]
            goto(video_url)
            views = int(view_scraper())
            
            view_change = views - view_lst[index]
            print('View Change:',view_change)

            if view_change > 5:
                       
                with open(video_path, mode='a', newline='') as video_csv: #a for append
                    csv_file = csv.writer(video_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    print('Writing CSV...', '\n')
                    csv_file.writerow([time.strftime('%H:%M', time.localtime()), time.time(), views ])
                    view_lst[index] = views
                    
                    
            else:
                print('not enough change')
                    

                

#------------------------------------------------------------------------------------------------------

def run():
    wait = 450
    cycle_start = time.time()
    view_log()
    cycle_end = time.time()
    cycle_time = cycle_end - cycle_start
    print('Cycle Time(s):', cycle_time)
    print('cycle complete', time.strftime('%H:%M', time.localtime()), '\n')
    goto('https://duckduckgo.com')
    print('Waiting',wait/60, '\n')
    #browser.close() keeps crashing
    time.sleep(wait) #30mins wait before  refresh


while True:
    try:
        run()
    except:
        print("Error")
        time.sleep(15)

