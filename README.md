# Youtube Playlist Duration API
Simple API to calculate the total duration of any public YouTube playlist.

### Run Locally

Clone the project:

```bash
  git clone https://github.com/pinovha/yt-api-playlist-duration.git
```

Navigate to the project directory:

```bash
  cd yt-api-playlist-duration
```

Install necessary libraries:
```bash
  pip install -r requirements.txt
```

Set your YouTube API key as an environment variable:

```bash
  export API_KEY="your-api-key-here"
```

Run script with playlist ID as an argument:

```bash
  python3 main.py PLAYLIST_ID
```

### Where to find the Playlist ID
Playlist ID is the part after `?list=` \
`https://www.youtube.com/playlist?list=PLAYLIST_ID` 

### API Request Breakdown

Here is how the requests are made:

|**Step**|**Description**|**Number of Requests**|
|----|----|----|
|**1** Fetch playlist videos| First request retrieves up to 50 videos from the playlist.| 1 request|
|**2** Fetch video durations| Second request retrieves the durations of those (up to 50) videos. | 1 request |
