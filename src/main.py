import pafyDemVids

vid_duration_list = []
vid_duration_secs = []

vid_duration_list = pafyDemVids.pafyAllTheVids(raw_input('Enter a song to search: '), raw_input('Max Results(~10?): '))

for videos in vid_duration_list:
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

print vid_duration_secs, "\n"
