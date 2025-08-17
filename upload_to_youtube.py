#!/usr/bin/env python3
"""
YouTube Video Upload Script

This script uploads a video to YouTube using the YouTube Data API v3.
It requires OAuth2 credentials to be set as environment variables.
"""

import argparse
import os
import sys
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# Explicitly tell the underlying HTTP transport library not to retry, since
# we are handling retry logic ourselves.
import httplib2
httplib2.RETRIES = 1

# Maximum number of times to retry before giving up.
MAX_RETRIES = 3

# Retriable exceptions.
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError)

# Retriable status codes.
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

# YouTube API scopes
YOUTUBE_UPLOAD_SCOPE = ["https://www.googleapis.com/auth/youtube.upload"]
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# Valid privacy statuses
VALID_PRIVACY_STATUSES = ("private", "public", "unlisted")


def get_authenticated_service():
    """
    Authenticate and build the YouTube service object using OAuth2 credentials
    from environment variables.
    """
    client_id = os.environ.get('YOUTUBE_CLIENT_ID')
    client_secret = os.environ.get('YOUTUBE_CLIENT_SECRET')
    refresh_token = os.environ.get('YOUTUBE_REFRESH_TOKEN')
    
    if not all([client_id, client_secret, refresh_token]):
        print("Error: Missing required YouTube API credentials in environment variables:")
        print("  - YOUTUBE_CLIENT_ID")
        print("  - YOUTUBE_CLIENT_SECRET") 
        print("  - YOUTUBE_REFRESH_TOKEN")
        sys.exit(1)
    
    credentials = Credentials(
        token=None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
        scopes=YOUTUBE_UPLOAD_SCOPE
    )
    
    # Refresh the token if needed
    if credentials.expired:
        credentials.refresh(Request())
    
    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, credentials=credentials)


def initialize_upload(youtube, file_path, title, description, tags=None, category_id="22", privacy_status="private"):
    """
    Upload a video to YouTube.
    
    Args:
        youtube: Authenticated YouTube service object
        file_path: Path to the video file
        title: Video title
        description: Video description  
        tags: List of tags (optional)
        category_id: YouTube category ID (default: 22 for "People & Blogs")
        privacy_status: Privacy setting (default: "private")
    """
    tags = tags or []
    
    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': category_id
        },
        'status': {
            'privacyStatus': privacy_status
        }
    }

    # Check if file exists
    if not os.path.isfile(file_path):
        print(f"Error: Video file not found: {file_path}")
        sys.exit(1)

    # Call the API's videos.insert method to create and upload the video.
    insert_request = youtube.videos().insert(
        part=",".join(body.keys()),
        body=body,
        media_body=MediaFileUpload(file_path, chunksize=-1, resumable=True)
    )

    return resumable_upload(insert_request)


def resumable_upload(insert_request):
    """
    Execute the upload request and retry on retriable errors.
    """
    response = None
    error = None
    retry = 0
    
    while response is None:
        try:
            print("Uploading file...")
            status, response = insert_request.next_chunk()
            if response is not None:
                if 'id' in response:
                    print(f"Video uploaded successfully! Video ID: {response['id']}")
                    print(f"Video URL: https://www.youtube.com/watch?v={response['id']}")
                    return response['id']
                else:
                    print(f"Upload failed with unexpected response: {response}")
                    sys.exit(1)
        except HttpError as e:
            if e.resp.status in RETRIABLE_STATUS_CODES:
                error = f"A retriable HTTP error {e.resp.status} occurred:\n{e.content}"
            else:
                print(f"A non-retriable HTTP error occurred:\n{e}")
                sys.exit(1)
        except RETRIABLE_EXCEPTIONS as e:
            error = f"A retriable error occurred: {e}"

        if error is not None:
            print(error)
            retry += 1
            if retry > MAX_RETRIES:
                print("Maximum retries exceeded. Upload failed.")
                sys.exit(1)

            import time
            import random
            max_sleep = 2 ** retry
            sleep_seconds = random.random() * max_sleep
            print(f"Sleeping {sleep_seconds} seconds and then retrying...")
            time.sleep(sleep_seconds)


def main():
    parser = argparse.ArgumentParser(description='Upload a video to YouTube')
    parser.add_argument('--file', required=True, help='Path to video file to upload')
    parser.add_argument('--title', required=True, help='Video title')
    parser.add_argument('--description', required=True, help='Video description')
    parser.add_argument('--tags', help='Comma-separated list of video tags')
    parser.add_argument('--category', default='22', help='YouTube category ID (default: 22)')
    parser.add_argument('--privacy', choices=VALID_PRIVACY_STATUSES, default='private',
                       help='Privacy status (default: private)')
    
    args = parser.parse_args()
    
    # Parse tags if provided
    tags = []
    if args.tags:
        tags = [tag.strip() for tag in args.tags.split(',')]
    
    try:
        youtube = get_authenticated_service()
        video_id = initialize_upload(
            youtube,
            args.file,
            args.title,
            args.description,
            tags,
            args.category,
            args.privacy
        )
        print(f"Upload completed successfully. Video ID: {video_id}")
    except HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred: {e.content}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()