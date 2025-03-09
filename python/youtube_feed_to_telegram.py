import feedparser
import requests
import os
import logging

# Configure logging to both file and console
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("youtube_to_telegram.log"),  # Log to file
        logging.StreamHandler()  # Log to console
    ]
)

# Configuration
CHANNEL_ID = os.getenv("CHANNEL_ID")  # YouTube Channel ID
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Telegram Bot Token
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")  # Telegram Chat ID
ALLOW_REPOST = os.getenv("ALLOW_REPOST", "false").lower() == "true"  # Allow re-posting
LAST_VIDEO_FILE = "last_video.txt"

# YouTube RSS Feed URL
RSS_FEED_URL = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"


def get_latest_video():
    """Fetch the latest video from the YouTube RSS feed."""
    try:
        feed = feedparser.parse(RSS_FEED_URL)
        if not feed.entries:
            logging.warning("No videos found in the RSS feed.")
            return None, None, None

        latest_entry = feed.entries[0]
        video_id = latest_entry.id.split(":")[-1]  # Extract Video ID
        video_url = latest_entry.link  # Extract Video URL
        video_title = latest_entry.title  # Extract Video Title
        logging.info(f"Latest video found: {video_title} ({video_url})")
        return video_id, video_url, video_title

    except Exception as e:
        logging.error(f"Error fetching RSS feed: {e}")
        return None, None, None


def get_last_posted_video():
    """Read the last posted video ID from the file."""
    if os.path.exists(LAST_VIDEO_FILE):
        try:
            with open(LAST_VIDEO_FILE, "r") as f:
                return f.read().strip()
        except Exception as e:
            logging.error(f"Error reading last video file: {e}")
            return None
    return None


def save_last_posted_video(video_id):
    """Save the last posted video ID to the file."""
    try:
        with open(LAST_VIDEO_FILE, "w") as f:
            f.write(video_id)
        logging.info("Last video ID updated.")
    except Exception as e:
        logging.error(f"Error saving last video ID: {e}")


def send_to_telegram(video_url, video_title):
    """Send the video link to Telegram."""
    message = f"🎥 *New YouTube Video Published!*\n\n📌 *{video_title}*\n🔗 {video_url}"
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
    }

    try:
        response = requests.post(telegram_url, json=payload)
        response.raise_for_status()  # Raises an error for bad responses (4xx, 5xx)
        logging.info("✅  Successfully sent video to Telegram.")
        return True
    except requests.exceptions.RequestException as e:
        logging.error(f"❌ Error sending message to Telegram: {e}")
        return False


def main():
    """Main function to check for new videos and send updates to Telegram."""
    video_id, video_url, video_title = get_latest_video()
    if not video_id or not video_url:
        logging.info("No new video detected.")
        return

    last_video_id = get_last_posted_video()

    if video_id != last_video_id or ALLOW_REPOST:
        if send_to_telegram(video_url, video_title):
            save_last_posted_video(video_id)
        else:
            logging.error("Failed to send message to Telegram.")
    else:
        logging.info("No new video detected, skipping Telegram update.")


if __name__ == "__main__":
    main()