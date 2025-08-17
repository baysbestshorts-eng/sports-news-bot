#!/usr/bin/env python3
"""
YouTube Video Upload Script

This script uploads a video to YouTube using OAuth 2.0 credentials stored as GitHub Actions secrets.
It uses the YouTube Data API v3 to perform the upload.

Required environment variables:
- YOUTUBE_CLIENT_ID: OAuth 2.0 client ID
- YOUTUBE_CLIENT_SECRET: OAuth 2.0 client secret  
- YOUTUBE_REFRESH_TOKEN: OAuth 2.0 refresh token for authentication
"""

import os
import sys
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


def get_youtube_service():
    """
    Create and return a YouTube API service object using stored credentials.
    """
    # Get credentials from environment variables
    client_id = os.environ.get('YOUTUBE_CLIENT_ID')
    client_secret = os.environ.get('YOUTUBE_CLIENT_SECRET')
    refresh_token = os.environ.get('YOUTUBE_REFRESH_TOKEN')
    
    if not all([client_id, client_secret, refresh_token]):
        raise ValueError("Missing required YouTube credentials. Please set YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET, and YOUTUBE_REFRESH_TOKEN environment variables.")
    
    # Create credentials object
    credentials = Credentials(
        token=None,  # Will be refreshed
        refresh_token=refresh_token,
        token_uri='https://oauth2.googleapis.com/token',
        client_id=client_id,
        client_secret=client_secret
    )
    
    # Refresh the token
    credentials.refresh(Request())
    
    # Build and return the YouTube service
    return build('youtube', 'v3', credentials=credentials)


def upload_video(video_file, title="Sports News Video", description="Automated sports news upload", tags=None, category_id='17'):
    """
    Upload a video to YouTube.
    
    Args:
        video_file (str): Path to the video file to upload
        title (str): Video title
        description (str): Video description
        tags (list): List of tags for the video
        category_id (str): YouTube category ID (17 = Sports)
    
    Returns:
        str: Video ID of the uploaded video, or None if upload failed
    """
    if tags is None:
        tags = ['sports', 'news', 'automated']
    
    try:
        # Get YouTube service
        youtube = get_youtube_service()
        
        # Define video metadata
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags,
                'categoryId': category_id
            },
            'status': {
                'privacyStatus': 'unlisted',  # Change to 'public' if you want public videos
                'selfDeclaredMadeForKids': False
            }
        }
        
        # Create media upload object
        media = MediaFileUpload(
            video_file,
            chunksize=-1,  # Upload in single request
            resumable=True,
            mimetype='video/*'
        )
        
        # Call the API's videos.insert method to create and upload the video
        insert_request = youtube.videos().insert(
            part=','.join(body.keys()),
            body=body,
            media_body=media
        )
        
        print(f"Uploading video: {title}")
        print(f"File: {video_file}")
        
        # Execute the upload
        response = insert_request.execute()
        
        video_id = response['id']
        print(f"Video uploaded successfully!")
        print(f"Video ID: {video_id}")
        print(f"Video URL: https://www.youtube.com/watch?v={video_id}")
        
        return video_id
        
    except HttpError as e:
        print(f"An HTTP error occurred: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def main():
    """
    Main function to handle command line arguments and upload video.
    """
    # Default video file path
    video_file = 'output.mp4'
    
    # Check if custom video file is provided as argument
    if len(sys.argv) > 1:
        video_file = sys.argv[1]
    
    # Check if video file exists
    if not os.path.isfile(video_file):
        print(f"Error: Video file '{video_file}' not found.")
        sys.exit(1)
    
    print(f"Starting YouTube upload process...")
    
    # Upload the video
    video_id = upload_video(
        video_file=video_file,
        title="Sports News Update",
        description="Latest sports news and updates delivered automatically.",
        tags=['sports', 'news', 'update', 'automated']
    )
    
    if video_id:
        print("Upload completed successfully!")
        sys.exit(0)
    else:
        print("Upload failed!")
        sys.exit(1)


if __name__ == '__main__':
    main()