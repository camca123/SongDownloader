#SongDownloader.py
#Written by Cameron Swinoga
#Meant to automatically search Youtube for a song, download it, and add metadata to it

differenceThreshold = 10
downloadFolder = 'C:\Users\Cameron\Desktop\Music\Maybe'

import pafyDemVids
import pafy

videoList = pafyDemVids.pafyAllTheVids(raw_input('Enter a song to search: '), raw_input('Max Results(~10?): '))
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
    print "Couldn't find any videos!"
    exit()

for vid in videoList:
    print vid[0].title, "\n", "S: ", vid[1], "\t", "Diff: ", vid[2]
print "\n\n"

print "Making streams..."
streams = []
n = 0
while (n < numGoodVideos):
    print n+1
    streams.append([videoList[n][0], videoList[n][0].getbestaudio()])
    n+=1
print "Done!", numGoodVideos, " good videos"
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
streams[0][1].download(downloadFolder, quiet=True)
#streams[0][1].download(downloadFolder)
print "Downloaded to", downloadFolder


