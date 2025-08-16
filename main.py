#!/usr/bin/env python3
"""
Sports News Bot - Main application entry point.

This bot fetches sports news updates and sends notifications via multiple channels:
- Discord (via webhook)
- Email (placeholder for future implementation)
- Other channels as needed
"""

import os
import time
from datetime import datetime
from sports_news.discord_notifier import send_discord_message


def simulate_email_notification(content):
    """
    Placeholder for existing email notification functionality.
    This ensures compatibility with existing features.
    """
    print(f"[EMAIL] Would send: {content}")


def fetch_sports_news():
    """
    Simulate fetching sports news from various sources.
    In a real implementation, this would fetch from APIs, RSS feeds, etc.
    """
    # Simulate some sports news updates
    sample_news = [
        "🏀 Lakers defeat Warriors 112-108 in overtime thriller!",
        "⚽ Manchester United signs new striker in record deal",
        "🏈 NFL Draft 2024: Top prospects to watch this season",
        "⚾ World Series Game 7: Historic matchup tonight!",
        "🎾 Wimbledon Final: Upset victory shakes tennis world"
    ]
    
    # In a real bot, this would return actual news data
    import random
    return random.choice(sample_news)


def send_notifications(content):
    """
    Send notifications via all configured channels.
    This maintains compatibility with existing notification methods
    while adding Discord integration.
    """
    # Existing email notifications (placeholder)
    simulate_email_notification(content)
    
    # New Discord webhook notifications
    send_discord_message(content)


def main():
    """
    Main application loop for the sports news bot.
    """
    print("🏆 Sports News Bot Starting...")
    print("📡 Checking for news updates...")
    
    # For demo purposes, we'll just fetch and send one news item
    # In a real implementation, this might run on a schedule
    try:
        news_update = fetch_sports_news()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Format the message with timestamp
        formatted_message = f"**Sports News Update** ({timestamp})\n{news_update}"
        
        print(f"📰 Found news: {news_update}")
        print("📤 Sending notifications...")
        
        # Send via all notification channels
        send_notifications(formatted_message)
        
        print("✅ Notifications sent successfully!")
        
    except Exception as e:
        error_msg = f"❌ Error in sports news bot: {e}"
        print(error_msg)
        # Still try to send error notification to Discord if possible
        try:
            send_discord_message(error_msg)
        except:
            pass


if __name__ == "__main__":
    main()