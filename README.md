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
name: Post YouTube Video to Telegram

on:
  push:
    branches:
      - main

jobs:
  post-video:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0 

      - name: Post YouTube Video to Telegram
        uses: pawanbahuguna/yt2tg/@v1.0.0
        env:
          CHANNEL_ID: ${{ secrets.YT_CHANNEL_ID }}
          TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
          ALLOW_REPOST: true
```

#### With Manual push

```yaml
name: Post YouTube Video to Telegram

on:
  push:
    branches:
      - main
  workflow_dispatch:  # Allows manual run
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
        uses: pawanbahuguna/yt2tg/@v1.0.0
        env:
          CHANNEL_ID: ${{ inputs.CHANNEL_ID || secrets.YT_CHANNEL_ID }}
          TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
          ALLOW_REPOST: ${{ inputs.ALLOW_REPOST || false }}
```

### Secrets

- `TELEGRAM_BOT_TOKEN`: The token for your Telegram bot. Store this as a secret in your GitHub repository.
- `TELEGRAM_CHAT_ID`: The ID of the Telegram chat where the message will be sent. Store this as a secret in your GitHub repository.
- `CHANNEL_ID`: The Channel ID of the YouTube channel. Store this as a secret in your GitHub repository. Also can be put manually. Check manual workflow example.


## License

This project is licensed under the MIT License.