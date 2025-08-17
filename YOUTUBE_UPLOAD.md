# YouTube Upload Workflow

This repository includes a GitHub Actions workflow for manually uploading videos to YouTube.

## Setup

To use the YouTube upload functionality, you need to configure the following GitHub repository secrets:

1. `YOUTUBE_CLIENT_ID` - Your YouTube API OAuth2 client ID
2. `YOUTUBE_CLIENT_SECRET` - Your YouTube API OAuth2 client secret  
3. `YOUTUBE_REFRESH_TOKEN` - Your YouTube API OAuth2 refresh token

### Getting YouTube API Credentials

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the YouTube Data API v3
4. Create OAuth2 credentials (Web application type)
5. Add your domain to authorized redirect URIs
6. Use the OAuth2 playground or a script to get a refresh token

## Usage

1. Go to the "Actions" tab in your GitHub repository
2. Select "Upload Video to YouTube" workflow
3. Click "Run workflow" 
4. Fill in the required inputs:
   - **Video file path**: Path to the video file (must be accessible in the runner)
   - **Title**: The title for your YouTube video
   - **Description**: The description for your YouTube video
5. Click "Run workflow" to start the upload

## Notes

- Videos are uploaded as "private" by default for security
- The workflow runs on Ubuntu and sets up Python 3.11
- All dependencies are automatically installed from requirements.txt
- The upload script includes retry logic for robust uploads
- Error handling provides clear feedback if credentials are missing or invalid

## File Structure

- `.github/workflows/upload.yml` - The GitHub Actions workflow
- `upload_to_youtube.py` - Python script that handles the YouTube upload
- `requirements.txt` - Python dependencies for the YouTube API