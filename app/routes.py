import feedparser
import json
import urllib
from urllib.request import urlopen, unquote, quote
from app import app
from flask import render_template, Flask, request


RSS_FEEDS = {
            'bbc':'http://feeds.bbci.co.uk/news/rss.xml',
            'cnn':'http://rss.cnn.com/rss/edition.rss',
            'fox':'http://feeds.foxnews.com/foxnews/latest',
            'iol':'http://www.iol.co.za/cmlink/1.640'
            }
WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&APPID=4d5a90b6a1f4a86986d156a72b892340"

@app.route('/')
@app.route('/index')
def index():
    query = request.args.get("publication")
    if not query or query.lower() not in RSS_FEEDS:
        publication = "bbc"
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    weather = get_weather("Hanoi,VN")
        
    return render_template('index.html',articles=feed['entries'], weather=weather)

def get_weather(query):
    query = urllib.request.quote(query)
    url = WEATHER_URL.format(query)
    data = urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get('weather'):
        weather = {'description': parsed['weather'][0]['description'],
                   'temperature': parsed['main']['temp'],
                   'city': parsed['name'],
                   'country': parsed['sys']['country']
                   }
    return weather






