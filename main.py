from apiclient.discovery import build
from collections import namedtuple
import time
import pafy

DEVELOPER_KEY = "AIzaSyDw7nsMtFcYUDylgGC2dbu4UHqQy8q-avI"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

search_videos = []
vid_url_list = []
pafy_vid_list = []
vid_duration_list = []

#-----------------------------------------------------------------------
def youtube_search(query, max_results):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)

    search_response = youtube.search().list(
        type = 'video',
        q = query,
        part = "id,snippet",
        maxResults = max_results
        ).execute()

    for search_result in search_response.get("items", []):
        search_videos.append(search_result["snippet"]["title"])
        vid_url_list.append("https://www.youtube.com/watch?v="+search_result["id"]["videoId"])
        video = pafy.new(vid_url_list[-1])
        pafy_vid_list.append(video)
#-----------------------------------------------------------------------

youtube_search(raw_input('Enter a song to search: '), 10)

for videos in pafy_vid_list:
    hrs = ''
    mins = ''
    secs = ''
    c = 0
    while c < len(videos.duration):
        if (videos.duration[c] != ':'):
            hrs += videos.duration[c]
        else:
            c+=1
            break
        c+=1
    while c < len(videos.duration):
        if (videos.duration[c] != ':'):
            mins += videos.duration[c]
        else:
            c+=1
            break
        c+=1
    while c < len(videos.duration):
        if (videos.duration[c] != ':'):
            secs += videos.duration[c]
        else:
            c+=1
            break
        c+=1
    vid_duration_list.append((int(hrs)*60*60)+(int(mins)*60)+int(secs))

print "\n".join(search_videos), "\n"
print vid_duration_list, "\n"
