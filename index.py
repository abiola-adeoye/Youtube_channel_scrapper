from flask import Flask, request, abort
from data_scraper import scrape_youtube
app = Flask(__name__)

@app.route("/index", methods=["GET"])
def hello_world():
    youtubeLink = request.args.get('link', '')

    if youtubeLink == '':
        abort(400)
    print("Link: " + youtubeLink)
    channel_info = scrape_youtube(youtubeLink)
    return channel_info

# once server is started inputing the channel link is done like "http://localhost:5000/index?link=[the youtube channel link]"
# the link should look like this with the input "http://localhost:5000/index?link=https://www.youtube.com/c/DatawithZach"
