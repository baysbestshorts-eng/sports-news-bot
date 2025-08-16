#!/usr/bin/env python3
"""
Simple test script to verify the Discord integration works correctly.
"""

import os
import sys
import tempfile
from unittest.mock import patch, MagicMock

# Add the current directory to Python path for imports
sys.path.insert(0, '/home/runner/work/sports-news-bot/sports-news-bot')

from sports_news.discord_notifier import send_discord_message


def test_discord_notifier_no_url():
    """Test Discord notifier behavior when no URL is set."""
    print("Testing Discord notifier without webhook URL...")
    
    # Ensure no webhook URL is set
    with patch.dict(os.environ, {}, clear=True):
        # Capture print output
        with patch('builtins.print') as mock_print:
            send_discord_message("Test message")
            mock_print.assert_called_with("No Discord webhook URL set.")
    
    print("✅ Test passed: Handles missing webhook URL correctly")


def test_discord_notifier_with_url():
    """Test Discord notifier behavior when URL is set."""
    print("Testing Discord notifier with webhook URL...")
    
    test_url = "https://discord.com/api/webhooks/test/test"
    
    with patch.dict(os.environ, {'DISCORD_WEBHOOK_URL': test_url}):
        with patch('requests.post') as mock_post:
            # Mock successful response
            mock_response = MagicMock()
            mock_response.status_code = 204
            mock_post.return_value = mock_response
            
            with patch('builtins.print') as mock_print:
                send_discord_message("Test message")
                
                # Verify requests.post was called correctly
                mock_post.assert_called_once_with(
                    test_url, 
                    json={"content": "Test message"}
                )
                
                # Verify success message was printed
                mock_print.assert_called_with("Message sent to Discord.")
    
    print("✅ Test passed: Sends message correctly when URL is provided")


def test_main_integration():
    """Test that main.py imports and uses Discord notifier correctly."""
    print("Testing main.py integration...")
    
    # Import main module
    import main
    
    # Test that the functions exist
    assert hasattr(main, 'send_notifications'), "send_notifications function should exist"
    assert hasattr(main, 'main'), "main function should exist"
    
    # Test that send_notifications calls Discord notifier
    with patch('main.simulate_email_notification') as mock_email:
        with patch('main.send_discord_message') as mock_discord:
            main.send_notifications("Test message")
            
            mock_email.assert_called_once_with("Test message")
            mock_discord.assert_called_once_with("Test message")
    
    print("✅ Test passed: main.py integrates Discord notifier correctly")


def main():
    """Run all tests."""
    print("🧪 Running Discord integration tests...\n")
    
    try:
        test_discord_notifier_no_url()
        test_discord_notifier_with_url()
        test_main_integration()
        
        print("\n🎉 All tests passed! Discord integration is working correctly.")
        return 0
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        return 1


if __name__ == "__main__":
    exit(main())