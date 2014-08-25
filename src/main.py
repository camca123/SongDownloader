import pafyDemVids

pafy_vids = []
vid_duration_secs = []

pafy_vids = pafyDemVids.pafyAllTheVids(raw_input('Enter a song to search: '), raw_input('Max Results(~10?): '))
print "\n\n"

for videos in pafy_vids:
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
    vid_duration_secs.append((int(hrs)*60*60)+(int(mins)*60)+int(secs))
    
vid_duration_secs.sort()


for i,vid in enumerate(pafy_vids):
    print vid.title, "\t", vid_duration_secs[i], "seconds"

print "\n\n"

differences = []
i = 0
while i < len(vid_duration_secs)-1:
    differences.append(vid_duration_secs[i+1]-vid_duration_secs[i])
    i+=1
#TODO: make a tuple containing the video, so that sorting the differences and etc, will stay with the video URL's

print differences
