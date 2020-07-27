import os
import json
five_candidates=[]
ten_candidates=[]
not_working = []
missed=0
all_songs = os.listdir("/home/kodhandarama/Desktop/Raga/Code/Audio_Analysis/lolol")
# all_songs.remove('.ipynb_checkpoints')
all_songs.sort()
print(all_songs)
for i in all_songs:
    song=os.path.join("/home/kodhandarama/Desktop/Raga/Code/Audio_Analysis/lolol",i,"vocals.wav")
    command= "python3 main.py --path '" +  song +"'"
    os.system(command)
    tonic_file = open('/home/kodhandarama/Desktop/Raga/Code/Audio_Analysis/Result4.json','r')
    data = json.load(tonic_file) 
    
    # for j in data :
    #     p_song=data[j]
    #     if(p_song["songname"]==i):
    #         songz=p_song
    # # print(song['Tonic'])
    # if(abs(songz["Tonic"]-songz["Our Tonic"])<=5):
    #     five_candidates.append(song["songname"])
    # elif (abs(songz["Tonic"]-songz["Our Tonic"])<=10):
    #     not_working.append(song["songname"])
    #     ten_candidates.append(song["songname"])
    # else:
    #     not_working.append(song["songname"])
    #     missed+=1

    # print(missed)
    # tonic_file.close()
    print("HIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")
    # print(command)


print(five_candidates)
print(not_working)
print(len(five_candidates))
print(len(not_working))