from webdriver_manager.chrome import ChromeDriverManager    #Important for using google chrome to scrape youtube data, it's the only browser that will work for this implementation
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait     # Implement a time delay to ensure the dynamic page is scrapped properly
from selenium.webdriver.chrome.options import Options      # will be required to stop the chrome application from popping up to perform task
from bs4 import BeautifulSoup

# function to scrape the about page of the youtube channel
def get_about_page(channel_name):
    chrome_options = Options()
    chrome_options.add_argument('--headless')   # this stops chrome from popping up as the page is being scraped
    driver = webdriver.Chrome(ChromeDriverManager().install(), options = chrome_options)
    driver.get('{}/about'.format(channel_name))    #the url is formatted into this string that takes it to the about page
    try:
        element = WebDriverWait(driver, 15) #implement a time delay of 15secs to scrape dynamic webpage
    except TimeoutException:
        print("Timed out waiting for page to load")
    content = driver.page_source.encode('utf-8').strip()
    driver.quit()
    soup = BeautifulSoup(content, 'lxml')          # Creates a soup object for us to easily extract the data we need
    return soup

#get channel name
def get_about_name(about_soup):   #pass in the soup object of the about page
    name = about_soup.find('yt-formatted-string', class_ = 'style-scope ytd-channel-name').text
    return name

# get channel description
def get_description(about_soup):
    description = about_soup.find('yt-formatted-string', id = 'description', class_='style-scope ytd-channel-about-metadata-renderer').text
    return description

# get location of channel
def get_location(about_soup):
    details_table = about_soup.find('tbody', class_='style-scope ytd-channel-about-metadata-renderer').text.split('\n')
    details_list = list(filter(lambda detail: detail != '', details_table))
    #list comprehension to return all the values that are not empty, if not included the indexing below will be incorrect
    location = details_list[-1]
    return location

# get date joined and views
def get_stats(about_soup):
    stats_container = about_soup.find('div', id='right-column')
    #The scraped data from youtube returns a text which needs to be split by the newline character. important info are at...
    #index 2 and 3, index 2 is the date joined and 3 is the total number of views
    stats = stats_container.text.split('\n')[2:4]
    return stats #the date of joining is in index 0 and views index 1

# get subscribers
def get_subscribers(about_soup):
    subscribers = about_soup.find('yt-formatted-string', id = 'subscriber-count').text
    return subscribers


# function to scrape the videos page of the youtube channel which has been sorted according to most popular (views highest to lowest)
def get_video_page(channel_name):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options = chrome_options)
    driver.get('{}/videos?view=0&sort=p&flow=grid'.format(channel_name))
    try:
        element = WebDriverWait(driver, 15) #implement a time delay of 15secs to scrape dynamic webpage
    except TimeoutException:
        print("Timed out waiting for page to load")
    content = driver.page_source.encode('utf-8').strip()
    soup = BeautifulSoup(content, 'lxml')
    return soup

# get titles of top 5 videos
def get_top_5_video_titles(video_soup):
    titles = []
    titles_name = video_soup.find_all('a', id = 'video-title', limit = 5)
    #returns a list of tags of the top five videos which need the title text extracted from this tag
    for title in titles_name:
        titles.append(title.text) #exrract title text and add to a list
    return titles

# get views of top 5 videos and year posted
def get_views_n_year(video_soup):
    views = []
    year_posted = []
    video_info = video_soup.find_all('span',class_ = 'style-scope ytd-grid-video-renderer', limit = 10)
    # two important information were placed together, limit of find_all function was multiplied by 2 for this
    # The for loop separates the information and saves in a list which is eventually returned to us
    for info in range(0,len(video_info),2):
        views.append(video_info[info].text)
        year_posted.append(video_info[info+1].text)
    return views, year_posted

def get_video_url(video_soup):
    video_link = []
    video_url = video_soup.find_all('a', id = 'video-title', limit = 5,href=True)
    for url in video_url:
        video_link.append('https://www.youtube.com'+url['href'])
    return video_link


def scrape_about_youtube(channel_name):
    about_page = get_about_page(channel_name)  # get soup object for about page

    # get channel name from about soup object
    channel_name = get_about_name(about_page)

    # get channel description
    channel_description = get_description(about_page)

    # get channel location
    channel_location = get_location(about_page)

    # get channel stats which are the date joined and total views, it is separated below
    channel_stats = get_stats(about_page)

    channel_date_joined = channel_stats[0]

    channel_total_views = channel_stats[1]

    # get total number of subscribers from channel
    channel_subscribers = get_subscribers(about_page)

    # dictionary data struct of data on about page
    about_info = {'channel_name': channel_name, 'channel_description': channel_description,
                  'channel_location': channel_location, 'channel_date_joined': channel_date_joined,
                  'channel_total_views': channel_total_views, 'channel_subscribers': channel_subscribers}

    return about_info


def scrape_video_youtube(channel_name):
    # information about each of the top five will be stored in a dictionary which will be stored in a list so each index of the list refers to all info on one of the top five videos
    video_info = {'title': 0, 'views': 0, 'year': 0, 'link': 0}
    top_five_videos = []
    video_page = get_video_page(channel_name)  # get soup object for video page

    # get the top five videos from the channel sorted by views
    video_top_title = get_top_5_video_titles(video_page)

    # get the number of views and year of release
    video_views, video_year = get_views_n_year(video_page)

    video_link = get_video_url(video_page)
    # dictionary data struct of data on top 5 videos from channel
    for index in range(len(video_top_title)):
        video_info['title'] = video_top_title[index]
        video_info['views'] = video_views[index]
        video_info['year'] = video_year[index]
        video_info['link'] = video_link[index]
        top_five_videos.append(video_info)

    top_five_info = {'top_five_title': top_five_videos}
    return top_five_info

# this calls the function to scrape all the data from the about page and video page and merges it into one dictionary
def scrape_youtube(channel):
    about = scrape_about_youtube(channel)
    video = scrape_video_youtube(channel)
    about.update(video)
    return about