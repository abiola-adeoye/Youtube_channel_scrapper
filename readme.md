###                                                     Youtube channel scraper

> This code scrapes data from the about page of a youtube channel as well as the top five most viewed videos from this channel and returns the data as a json data

> a link to the youtube channel without clicking on any side link within the channel (home,videos,playlist,about) should be provided as input

> The expected maximum time to scrape all this information from a youtube channel once run is 40 secs 

> 'chrome_option' object is used to stop the chrome application from popping up while scrapping the data, if you want to see the chrome application pop up while scrapping the data, you can comment out all instances of 'chrome_options' 

>once server is started inputing the channel link is done like "[server port]/index?link=[the youtube channel link]"
 the link should look like this with the input "http://localhost:5000/index?link=https://www.youtube.com/c/DatawithZach"
