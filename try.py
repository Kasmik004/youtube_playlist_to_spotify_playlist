import youtube_dl

def get_video_title(video_url):
    # Options for youtube_dl
    ydl_opts = {
        'quiet': True,  # Disable verbose output
        'simulate': True,  # Simulate download
        'gettitle': True,  # Get video title
    }

    # Create a youtube_dl object
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            # Download metadata
            info = ydl.extract_info(video_url, download=False)
            # Extract video title
            video_title = info.get('title', None)
            return video_title
        except youtube_dl.DownloadError as e:
            print(f"Error: {e}")
            return None

# Example usage
video_url = 'https://www.youtube.com/watch?v=RCwAFS6S9O4'  # Example video URL
video_title = get_video_title(video_url)
if video_title:
    print("Video title:", video_title)
else:
    print("Video title not found.")
