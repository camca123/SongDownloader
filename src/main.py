#SongDownloader.py
#Written by Cameron Swinoga
#Meant to automatically search Youtube for a song, download it, and add metadata to it

import pafyDemVids
import videoFinderDownloader
import file_reader
import pafy
import re

downloadFolder = file_reader.readFromFile("musicDirectory")
print "Download Folder is:", downloadFolder
if (downloadFolder == "Err"):
        print "Error with config file!"
        exit()

def searchVideos():
    differenceThreshold = int(file_reader.readFromFile("differenceThreshold"))
    print "Difference threshold:", differenceThreshold

    videoList = pafyDemVids.pafyAllTheVids(raw_input("Enter a song to search: "), raw_input("Max Results(~5?): "))
    #[pafyVideo, duration in seconds, time difference between videos]
    print "\n"
    videoFinderDownloader.downloadBestVideo(videoList, downloadFolder, differenceThreshold)

def organizeMusic():
    os.system("beet import -i "+downloadFolder)

def downloadPlaylist():
    playlist = pafy.get_playlist(raw_input("Enter playlist URL: "))
    
    for i in range(0, len(playlist['items'])):
        print playlist['items'][i]['pafy'].title
        stream = playlist['items'][i]['pafy'].getbestaudio("m4a")
        print "Downloading!"
        stream.download(downloadFolder, quiet = True)
        print "Downloaded to", downloadFolder

downloadPlaylist()
