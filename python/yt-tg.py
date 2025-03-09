import os
import requests
import logging
from dotenv import load_dotenv

# Enable logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# Load environment variables
load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
CHANNEL_ID = os.getenv("CHANNEL_ID")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not all([YOUTUBE_API_KEY, CHANNEL_ID, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID]):
    logging.error("Missing one or more environment variables. Check .env file or GitHub Secrets.")
    exit(1)

def get_latest_video():
    url = f"https://www.googleapis.com/youtube/v3/search?key={YOUTUBE_API_KEY}&channelId={CHANNEL_ID}&part=snippet,id&order=date&maxResults=1"
    
    logging.info(f"Fetching latest video from URL: {url}")
    
    response = requests.get(url)
    
    if response.status_code != 200:
        logging.error(f"Error fetching YouTube data: {response.status_code}, Response: {response.text}")
        return None
    
    data = response.json()
    logging.debug(f"YouTube API Response: {data}")

    if "items" in data and len(data["items"]) > 0:
        video_id = data["items"][0]["id"].get("videoId")
        if video_id:
            video_url = f"https://youtu.be/{video_id}"
            logging.info(f"Latest video found: {video_url}")
            return video_url
        else:
            logging.warning("No videoId found in response.")
    else:
        logging.warning("No videos found for this channel.")
    
    return None

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}

    logging.info(f"Sending message to Telegram: {message}")
    
    response = requests.post(url, data=data)
    
    if response.status_code == 200:
        logging.info("Message sent successfully to Telegram.")
    else:
        logging.error(f"Failed to send message to Telegram: {response.status_code}, Response: {response.text}")

# Run script
latest_video = get_latest_video()
if latest_video:
    send_to_telegram(f"👉 Checkout the latest video: {latest_video}")
else:
    logging.warning("No new video found. Skipping Telegram notification.")
