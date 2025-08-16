# Sports News Bot

A Python bot that fetches sports news updates and sends notifications to multiple channels including Discord webhooks and email.

## Features

- 🏆 Fetches sports news from various sources
- 📧 Email notifications (placeholder for future implementation)
- 💬 Discord webhook notifications
- 🔄 Extensible notification system
- ⚙️ Environment-based configuration

## Setup

### Prerequisites

- Python 3.7+
- `requests` library for HTTP calls

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/baysbestshorts-eng/sports-news-bot.git
   cd sports-news-bot
   ```

2. Install dependencies:
   ```bash
   pip install requests
   ```

### Configuration

#### Discord Webhook Setup

To enable Discord notifications, you need to set up a Discord webhook:

1. **Create a Discord Webhook:**
   - Go to your Discord server
   - Navigate to Server Settings → Integrations → Webhooks
   - Click "New Webhook"
   - Choose the channel where you want notifications
   - Copy the webhook URL

2. **Set Environment Variable:**
   ```bash
   export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN"
   ```

   **Required Environment Variables:**
   - `DISCORD_WEBHOOK_URL`: Discord webhook URL for sending notifications

   **Note:** If `DISCORD_WEBHOOK_URL` is not set, Discord notifications will be skipped with a warning message.

## Usage

### Running the Bot

```bash
python main.py
```

### Example Output

```
🏆 Sports News Bot Starting...
📡 Checking for news updates...
📰 Found news: 🏀 Lakers defeat Warriors 112-108 in overtime thriller!
📤 Sending notifications...
[EMAIL] Would send: **Sports News Update** (2024-01-15 10:30:45)
🏀 Lakers defeat Warriors 112-108 in overtime thriller!
Message sent to Discord.
✅ Notifications sent successfully!
```

## GitHub Actions Setup

For automated deployments and scheduled runs, you can set up GitHub Actions:

### 1. Store Discord Webhook as a Secret

1. Go to your repository on GitHub
2. Navigate to Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Name: `DISCORD_WEBHOOK_URL`
5. Value: Your Discord webhook URL
6. Click "Add secret"

### 2. Example GitHub Actions Workflow

Create `.github/workflows/sports-news-bot.yml`:

```yaml
name: Sports News Bot

on:
  schedule:
    # Run every hour at minute 0
    - cron: '0 * * * *'
  workflow_dispatch: # Allow manual triggers

jobs:
  send-news-update:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
      
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install requests
        
    - name: Run sports news bot
      env:
        DISCORD_WEBHOOK_URL: ${{ secrets.DISCORD_WEBHOOK_URL }}
      run: python main.py
```

### 3. Security Best Practices

- **Never commit webhook URLs to your repository**
- **Always use GitHub Secrets for sensitive data**
- **Use environment variables for configuration**
- **Consider using webhook validation for production use**

## Development

### Project Structure

```
sports-news-bot/
├── main.py                      # Main application entry point
├── sports_news/                 # Package directory
│   └── discord_notifier.py      # Discord webhook functionality
├── .github/                     # GitHub Actions workflows (optional)
│   └── workflows/
│       └── sports-news-bot.yml
└── README.md                    # This file
```

### Adding New Notification Channels

To add new notification channels:

1. Create a new module in the `sports_news/` directory
2. Implement a function similar to `send_discord_message(content)`
3. Import and call it in the `send_notifications()` function in `main.py`

### Testing

You can test the Discord integration by setting the webhook URL and running:

```bash
export DISCORD_WEBHOOK_URL="your_webhook_url_here"
python main.py
```

## API Reference

### `send_discord_message(content)`

Sends a message to Discord via webhook.

**Parameters:**
- `content` (str): The message content to send

**Environment Variables:**
- `DISCORD_WEBHOOK_URL`: Discord webhook URL (required)

**Returns:**
- None

**Behavior:**
- If webhook URL is not set, prints a warning and returns early
- On success, prints "Message sent to Discord."
- On error, prints error details

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source. Please check the repository for license details.