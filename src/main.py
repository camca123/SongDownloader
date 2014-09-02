import pafyDemVids

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
            temp = videoList[n][1]
            videoList[n][1] = videoList[n+1][1]
            videoList[n+1][1] = temp
            swapped = True
        n+=1

n = 0
while n < len(videoList)-1:
    videoList[n][2] = videoList[n+1][1]-videoList[n][1]
    n+=1

print "\n\n"
for vid in videoList:
    print vid[0].title, "\n", "S: ", vid[1], "\t", "Diff: ", vid[2]
