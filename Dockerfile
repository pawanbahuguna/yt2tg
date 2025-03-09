FROM python:3.9

WORKDIR /app

COPY python/requirements.txt .
RUN pip3 install -r requirements.txt

COPY python/youtube_feed_to_telegram.py .

ENTRYPOINT ["python3", "/app/youtube_feed_to_telegram.py"]
