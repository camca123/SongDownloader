from apiclient.discovery import build
import time

DEVELOPER_KEY = "AIzaSyDw7nsMtFcYUDylgGC2dbu4UHqQy8q-avI"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


youtube_search("google", 1)

print "\n".join(search_videos), "\n"

print "\n".join(video_ids), "\n"
print "\n".join(video_lengths), "\n"
