import feedparser
import pprint
import requests
import trafilatura 
import json
import os
from pathlib import Path


#feedSource = "CGTN WORLD NEWS"
#d = feedparser.parse("https://www.cgtn.com/subscribe/rss/section/world.xml")

#data-model
#world_news_feed = {
    #"source": feedSource,
    #"latest_feed": {
        #"headline": d.entries[0].title,
        #"description": d.entries[0].description,
        #"link": d.entries[0].link,
        #"date_published": d.entries[0].published,
   # },
#}

#pprint.pprint(world_news_feed)


#persistent state
history = Path(__file__).parent / "history.json"


#if history.exists():
    #data = history.read_text()

#else:
    #print("history.json file not found")


#config
feeds = [
    {"feed_source" : "CGTN WORLD NEWS", "feed_link" : "https://www.cgtn.com/subscribe/rss/section/world.xml"},
    {"feed_source" : "BBC NEWS", "feed_link" : "http://newsrss.bbc.co.uk/rss/newsonline_uk_edition/front_page/rss.xml"}
]


#logic ¬
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


#pprint.pprint(fetch_and_shape("", ""))



#state
#turn the list data into text (json.dumps) and write to file 
def append_to_jsonl(history, aggregate_feed):
    with open(history, "a", encoding="utf-8") as f:
        for item in aggregate_feed:
            f.write(json.dumps(item) + os.linesep)

#pprint.pprint(history_content)

#convert json text data to python list 
def load_jsonl_to_list(history):
    with open(history, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]

#function to fetch raw html from links in news_feed
def fetch_raw_link_content(history_list):
    link_contents = []
    for link in history_list:
            result = link["latest_feed"]["link"]
            r = requests.get(result)
            content = r.text
            link_contents.append(content)
            #print(content)
            r.raise_for_status()
    return link_contents   
#pprint.pprint(fetch_raw_link_content(history_list))

#function to extract clean text from raw html in link_contents
def extract_clean_prose_with_meta(history_list, raw_html_payloads):
    content_text = []
    for feed_metadata, raw_html in zip(history_list, raw_html_payloads):
        clean_content = trafilatura.extract(raw_html, output_format="markdown",)
        
        if clean_content is not None:
            source = feed_metadata.get("source", "UNKNOWN SOURCE")
            headline = feed_metadata["latest_feed"].get("headline", "NO HEADLINE")
            date = feed_metadata["latest_feed"].get("date_published", "NO DATE")

            meta_wrapped_story = (
                f"=== ARTICLE SOURCE: {source} ===\n"
                f"HEADLINE: {headline}\n"
                f"PUBLISHED: {date}\n"
                f"--- CONTENT BEGIN ---\n"
                f"{clean_content}\n"
                f"=== END OF ARTICLE ===\n"
            )
            content_text.append(meta_wrapped_story)
    return content_text

#format clean stories off the list elements (string notations) into raw texts
def format_cleaned_stories(clean_stories_with_meta):
    return "\n" + "\n".join(clean_stories_with_meta)








def pipeline_runner():
    aggregate_feed = []
    for feed in feeds:
        result = fetch_and_shape(feed["feed_source"], feed["feed_link"])
        aggregate_feed.append(result)

    append_to_jsonl(history, aggregate_feed)

    # read state to memory for use in futher computation (primming)
    #with open(history, "r", encoding="utf=8") as f:
        #history_content = f.read()

    #history_list = load_jsonl_to_list(history)
    #raw_html_payloads = fetch_raw_link_content(history_list)
    #clean_stories_with_meta = extract_clean_prose_with_meta(history_list, raw_html_payloads)
    #return clean_stories_with_meta

    return aggregate_feed



if __name__ == "__main__":
    stories = pipeline_runner()
    print(format_cleaned_stories(stories))

    
    


