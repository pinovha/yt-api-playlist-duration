from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import timedelta
from isodate import parse_duration
import os, sys

# In the terminal, set the environment variable:
# export API_KEY="your-api-key-here"

# Fetch the API_KEY from the environment
API_KEY = os.getenv("API_KEY")

# Check if the number of command-line arguments is exactly 2
if len(sys.argv) != 2:
    print(f"""
          This program requires exactly one argument after script name to run correctly:
          Usage: file_name.py playlist_id
          """)
    sys.exit(1)

# Assign second argument from command-line (the one after the script name) to the variable 'PLAYLIST_ID'
PLAYLIST_ID = sys.argv[1]

API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

# Build the Youtube API client
youtube = build(API_SERVICE_NAME, API_VERSION, developerKey=API_KEY)

# Initialize without a page token for the first iteration
next_page_token = None

# Initialize total_duration variable as a timedelta object
# to keep track of the total duration of the playlist
total_duration = timedelta()

# Loop through all items in the playlist, one page at a time
while True:
    try:
        response = youtube.playlistItems().list(
            # Ask for 'contentDetails' to get video metadata
            part="contentDetails",
            playlistId=PLAYLIST_ID,
            # maxResults cannot exceed 50 (API limit)
            maxResults=50,
            # Use pageToken to get next page of results
            pageToken=next_page_token
        ).execute()

        # Initialize a list to store video IDs 
        videos_ids = []
        
        # Iterate through each video in the playlist response
        for item in response['items']:
            # Extract video ID from the playlist item and append to the list
            videos_ids.append(item['contentDetails']['videoId'])
            
        try:
            # Fetch video details using video ID
            video_response = youtube.videos().list(
                # Ask for details of the video
                part="contentDetails",
                # Combine all collected 50 video IDs into a single string, separated by commas
                id=','.join(videos_ids)
            ).execute()

        # Display error message and continue processing
        except HttpError as error:
            print(f"\nFailed to fetch video details. \n\nError: {error}\n")
            continue

        # Iterate through each item in video_response
        for item in video_response['items']:
            # Extract the duration data from the video_response, which is in 'ISO 8601 duration format'
            duration_iso = item['contentDetails']['duration']

            # Convert ISO 8601 duration string intro a Python timedelta object
            duration = parse_duration(duration_iso)

            # Add the duration of current video to the total_duration
            total_duration += duration

        # Get nextPageToken from response to fetch the next page of results
        next_page_token = response.get('nextPageToken')

        # If there is no nextPageToken, we have iterated through all items in the playlist
        if not next_page_token:

            # Convert total_duration to seconds and store the result as an integer
            total_seconds = int(total_duration.total_seconds())

            # Convert total_seconds into hours, minutes and seconds
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60

            # Print the total duration of all videos in the playlist
            print(f"{hours} Hours {minutes} Minutes {seconds} Seconds")

            break

    # Break the loop if an error occurs to stop further processing
    except HttpError as error:
        print(f"\nFailed to fetch playlist items: \n\nError: {error}\n")
        break