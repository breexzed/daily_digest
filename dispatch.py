import os
import sys
import requests
from news_ingest import pipeline_runner
from prompt import summarize_article
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
MY_CHAT_ID = os.getenv("MY_CHAT_ID")
url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"


def format_data_model_payload(feed_item):
    """
    Transform the raw dict data model to clean plain-text
    """
    source = feed_item.get("source", "UNKNOWN").upper()
    feed_data = feed_item.get("latest_feed", {})

    headline = feed_data.get("headline", "No Headline.")
    desc = feed_data.get("description", "No description available.")
    link = feed_data.get("link", "No link available")
    date = feed_data.get("date_published", "")


    card = (
        f" Source: [{source}]\n\n"
        f" Headline: {headline}\n\n"
        f" Description: {desc}\n\n"
        f" {date}\n\n"
        f" Link: {link}\n\n"
    )
    return card

def main():
    #check for executiion flags
    use_ai = "--ai" in sys.argv

    print("Executing pipeline...")

    aggregate_feed = pipeline_runner()


    for item in aggregate_feed:
        if use_ai:
            print("AI flag detected. Routing data model through LLM engine...")

            #convert the dict to a string so the llm can read it
            data_string = str(item)     
            message_text = summarize_article(data_string)
        
        else:
            print("Direct Dispatch. Formatting data model raw payload...")
            message_text = format_data_model_payload(item)

    
        #Truncation safety grid
        if len(message_text) > 4096:
            print(f"Warning: AI still exceeds limits ({len(message_text)} chars). Clipping.")
            message_text = message_text[:4090] + "\n..."

        payload = {
            "chat_id" : MY_CHAT_ID,
            "text"  : message_text,
            }
        
    
        try:
            response = requests.post(url, data=payload, timeout=10)
            print(f"Server Status Code: {response.status_code}")
            #print(f"Server Response: {response.text}")

            if response.status_code != 200:
                print(f"Telegram API ERROR: {response.text}")
        except requests.exceptions.RequestException as e:
             print(f"Network Pipe Chocked: {e}")

    

if __name__ == "__main__":
    main()













