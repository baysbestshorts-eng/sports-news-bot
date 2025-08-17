import argparse
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', required=True, help='Path to video file')
    parser.add_argument('--title', required=True, help='Video title')
    parser.add_argument('--description', required=True, help='Video description')
    args = parser.parse_args()

    creds = Credentials(
        None,
        refresh_token=os.environ.get('YOUTUBE_REFRESH_TOKEN'),
        client_id=os.environ.get('YOUTUBE_CLIENT_ID'),
        client_secret=os.environ.get('YOUTUBE_CLIENT_SECRET'),
        token_uri='https://oauth2.googleapis.com/token'
    )
    if not creds.valid and creds.refresh_token:
        creds.refresh(Request())

    youtube = build('youtube', 'v3', credentials=creds)

    body = {
        'snippet': {
            'title': args.title,
            'description': args.description,
            'categoryId': '22',  # People & Blogs
        },
        'status': {
            'privacyStatus': 'private',
        }
    }

    media = MediaFileUpload(args.file, mimetype='video/*', resumable=True)
    request = youtube.videos().insert(
        part=','.join(body.keys()),
        body=body,
        media_body=media
    )
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploaded {int(status.progress() * 100)}%")
    print(f"Upload Complete! Video ID: {response['id']}")

if __name__ == '__main__':
    main()
