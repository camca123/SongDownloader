from apiclient.discovery import build
import pafy

DEVELOPER_KEY = "AIzaSyDw7nsMtFcYUDylgGC2dbu4UHqQy8q-avI"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

search_videos = []
vid_url_list = []
pafy_vid_list = []

def pafyAllTheVids(query, max_results):
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
        pafy_vid_list.append([video, -1, 5000])
    return pafy_vid_list
