import feedparser
import pprint
import requests
import trafilatura 
import json
import os
from pathlib import Path

feed_source = "CGTN WORLD NEWS"
feed_link = "https://www.cgtn.com/subscribe/rss/section/world.xml"
    

def fetch_and_shape(feed_source, feed_link):                               #parameterization
    
   d = feedparser.parse(feed_link)

   if not d.entries:
       print(f"Warning: Feed Stream for {feed_source} is completely empty or down currently")
       return {
           "source" : feed_source,
           "latest_Feed" : {
               "headline" : "Feed Unavailable",
               "description" : "Could not extract data from feed source",
               "link" : feed_link,
               "date_published" : "N/A"
           }
       }

   news_feed = {
        "source" : feed_source,
        "latest_feed" : {
            "headline" : d.entries[0].title,
            "description" : d.entries[0].description, 
            "link" : d.entries[0].link, 
            "date_published" : d.entries[0].published 
        }
    }

   return news_feed


print(fetch_and_shape(feed_source, feed_link))

