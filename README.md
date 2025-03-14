# Post YouTube Video Links to Telegram [NO YouTube API Required]

Post YouTube Video Links to Telegram without using YouTube API.

## Usage

This GitHub Action allows you to post YouTube video links to a Telegram channel or chat without using the YouTube API. 

### Inputs

- `CHANNEL_ID`: YouTube channel ID
- `TELEGRAM_BOT_TOKEN`: The token for your Telegram bot.
- `TELEGRAM_CHAT_ID`: The ID of the Telegram chat where the message will be sent.
- `ALLOW_REPOST`: Defaults to `false`. Set to `true` if you want to post the same link again.


### Example Workflow

```yaml
permissions:
  contents: write

name: Post YouTube Video to Telegram

on:
  schedule:
    - cron: '0 * * * *' # Runs every hour

jobs:
  post-video:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0 

      - name: Post YouTube Video to Telegram
        uses: pawanbahuguna/yt2tg/@1.0.0
        env:
          CHANNEL_ID: ${{ secrets.YT_CHANNEL_ID }}
          TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
          ALLOW_REPOST: true # optional, defaults to false

      - name: Commit and Push Changes
        if: always()  # Ensure this step runs even if the previous step fails
        run: |
          git config --global user.name "GitHub Actions"
          git config --global user.email "actions@github.com"
          git add last_video.txt
          git diff --quiet && git diff --staged --quiet || git commit -m "Update last_video.txt with latest video ID"
          git push
```

#### With Manual push

```yaml
permissions:
  contents: write

name: Post YouTube Video to Telegram

on:
  schedule:
    - cron: '0 * * * *' # Runs every hour

  workflow_dispatch:  # Allows manual run with custom YouTube ID
    inputs: 
      CHANNEL_ID:
        description: 'YouTube Channel ID'
        required: true
        type: string
      ALLOW_REPOST:
        description: 'Allow re-posting the same video link'
        required: false
        type: boolean
        default: false
jobs:
  post-video:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0 

      - name: Post YouTube Video to Telegram
        uses: pawanbahuguna/yt2tg/@1.0.0
        env:
          CHANNEL_ID: ${{ inputs.CHANNEL_ID || secrets.YT_CHANNEL_ID }}
          TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
          ALLOW_REPOST: ${{ inputs.ALLOW_REPOST || false }} # optional, defaults to false

      - name: Commit and Push Changes
        if: always()  # Ensure this step runs even if the previous step fails
        run: |
          git config --global user.name "GitHub Actions"
          git config --global user.email "actions@github.com"
          git add last_video.txt
          git diff --quiet && git diff --staged --quiet || git commit -m "Update last_video.txt with latest video ID"
          git push
```

### Secrets

- `TELEGRAM_BOT_TOKEN`: The token for your Telegram bot. Store this as a secret in your GitHub repository.
- `TELEGRAM_CHAT_ID`: The ID of the Telegram chat where the message will be sent. Store this as a secret in your GitHub repository.
- `CHANNEL_ID`: The Channel ID of the YouTube channel. Store this as a secret in your GitHub repository. Also can be put manually. Check manual workflow example.


## License

This project is licensed under the MIT License.