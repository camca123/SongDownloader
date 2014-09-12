#SongDownloader
#Written by Cameron Swinoga
#Meant to automatically search Youtube for a song, download it, and add metadata to it

import pafyDemVids
import videoFinderDownloader
import file_reader
import pafy
import os

downloadFolder = ""

def init():
    global downloadFolder
    downloadFolder = file_reader.readFromFile("musicDirectory")
    print "Download Folder is:", downloadFolder
    if (downloadFolder == "Err"):
            print "Error with config file!"
            exit()

def searchVideos(query, maxResults):
    init()
    global downloadFolder
    print "Search:", query
    differenceThreshold = int(file_reader.readFromFile("differenceThreshold"))
    print "Difference threshold:", differenceThreshold

    videoList = pafyDemVids.pafyAllTheVids(query, maxResults)
    #[pafyVideo, duration in seconds, time difference between videos]
    videoFinderDownloader.downloadBestVideo(videoList, downloadFolder, differenceThreshold)

def organizeMusic():
    init()
    global downloadFolder
    os.system("beet import -i "+downloadFolder)

def downloadPlaylist(playlistURL):
    init()
    global downloadFolder
    playlist = pafy.get_playlist(playlistURL)
    
    for i in range(0, len(playlist['items'])):
        print playlist['items'][i]['pafy'].title
        stream = playlist['items'][i]['pafy'].getbestaudio("m4a")
        print "Downloading!"
        stream.download(downloadFolder, quiet = True)
        print "Downloaded to", downloadFolder
