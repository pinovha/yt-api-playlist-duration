from googleapiclient.discovery import build
from datetime import timedelta
from isodate import parse_duration
import os

# In the terminal, set the environment variable:
# export API_KEY="your-api-key-here"

# Fetch the API_KEY from the environment
API_KEY = os.getenv("API_KEY")

API_SERVICE_NAME = "youtube"
API_VERSION = "v3"
PLAYLIST_ID = "PLOYHgt8dIdozG4A2A1lFj5UBJJ4ywl0FV"

# Build the Youtube API client
youtube = build(API_SERVICE_NAME, API_VERSION, developerKey=API_KEY)

# Initialize without a page token for the first iteration
next_page_token = None

# Video listing starts at index 1
index = 1

# Loop through all items in the playlist, one page at a time
while True:
    response = youtube.playlistItems().list(
        # Ask for 'snippet' to get video metadata
        part="snippet",
        playlistId=PLAYLIST_ID,
        # maxResults cannot exceed 50 (API limit)
        maxResults=50,
        # Use pageToken to get next page of results
        pageToken=next_page_token
    ).execute()

    # Iterate through each video in the playlist response
    for item in response['items']:
        # Extract the title of the video
        title = item['snippet']['title']
        # Extract video ID from the playlist item
        video_id = item['snippet']['resourceId']['videoId']
    
        # Fetch video details using video ID
        video_response = youtube.videos().list(
            # Ask for details of the video
            part="contentDetails",
            # Identyify the video by its ID
            id=video_id
        ).execute()

        print(f"{index} - {title}")
        # Increment the index by 1 to keep track of the video number 
        index +=1
    
    # Get nextPageToken from response to fetch the next page of results
    next_page_token = response.get('nextPageToken')
    # If there is no nextPageToken, we have iterated through all items in the playlist
    if not next_page_token:
        break