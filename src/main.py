#SongDownloader.py
#Written by Cameron Swinoga
#Meant to automatically search Youtube for a song, download it, and add metadata to it

import pafyDemVids
import file_reader
import pafy
import os
import re

downloadFolder = file_reader.readFromFile("musicDirectory")
differenceThreshold = int(file_reader.readFromFile("differenceThreshold"))

print "Download Folder is:", downloadFolder
print "Difference threshold:", differenceThreshold

if (downloadFolder == "Err"):
    print "Error with config file!"
    exit()

videoList = pafyDemVids.pafyAllTheVids(raw_input('Enter a song to search: '), raw_input('Max Results(~5?): '))
#[pafyVideo, duration in seconds, time difference between videos]
print "\n\n"

for videos in videoList:
    hrs = ''
    mins = ''
    secs = ''
    c = 0
    while c < len(videos[0].duration):
        if (videos[0].duration[c] != ':'):
            hrs += videos[0].duration[c]
        else:
            c+=1
            break
        c+=1
    while c < len(videos[0].duration):
        if (videos[0].duration[c] != ':'):
            mins += videos[0].duration[c]
        else:
            c+=1
            break
        c+=1
    while c < len(videos[0].duration):
        if (videos[0].duration[c] != ':'):
            secs += videos[0].duration[c]
        else:
            c+=1
            break
        c+=1
    videos[1] = (int(hrs)*60*60)+(int(mins)*60)+int(secs)
    
swapped = True
while(swapped):
    swapped = False
    n = 0
    while(n < len(videoList)-1):
        if (videoList[n][1] > videoList[n+1][1]):
            temp = videoList[n]
            videoList[n] = videoList[n+1]
            videoList[n+1] = temp
            swapped = True
        n+=1

n = 0
while n < len(videoList)-1:
    videoList[n][2] = videoList[n+1][1]-videoList[n][1]
    n+=1

swapped = True
while(swapped):
    swapped = False
    n = 0
    while(n < len(videoList)-1):
        if (videoList[n][2] > videoList[n+1][2]):
            temp = videoList[n]
            videoList[n] = videoList[n+1]
            videoList[n+1] = temp
            swapped = True
        n+=1

numGoodVideos = 0
for vid in videoList:
    if (vid[2] < differenceThreshold):
        numGoodVideos += 1
if (numGoodVideos == 0):
    print "Couldn't find any good songs!"
    exit()

for vid in videoList:
    print vid[0].title, "\n", "S: ", vid[1], "\t", "Diff: ", vid[2]
print "\n\n"

print "Making streams..."
streams = []
n = 0
while (n < numGoodVideos):
    streams.append([videoList[n][0], videoList[n][0].getbestaudio("m4a")])
    n+=1
print "Done!", numGoodVideos, "good videos"
#Stream list: [pafy video, video stream]

print "Organizing by bitrate..."
swapped = True
while(swapped):
    swapped = False
    n = 0
    while(n < numGoodVideos-1):
        if (streams[n][1].rawbitrate > streams[n+1][1].rawbitrate):
            temp = streams[n]
            streams[n] = streams[n+1]
            streams[n+1] = temp
            swapped = True
        n+=1
print "Done!"

def mycb(total, recvd, ratio, rate, eta):
    print eta, " seconds left..."

print "Downloading!"
print repr(downloadFolder)
streams[0][1].download(downloadFolder, quiet=True)
print "Downloaded to", downloadFolder

print "Starting beets to add metadata... Title is \"", streams[0][0].title, "\""
os.system("beet import "+downloadFolder)
