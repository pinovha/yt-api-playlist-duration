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
PLAYLIST_ID = ""

youtube = build(API_SERVICE_NAME, API_VERSION, developerKey='API_KEY')

