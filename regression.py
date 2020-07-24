import os

all_songs = os.listdir("/home/kodhandarama/Desktop/Raga/Code/Tonic_source_separation")
# all_songs.remove('.ipynb_checkpoints')
all_songs.sort()
print(all_songs)
for i in all_songs:
    song=os.path.join("/home/kodhandarama/Desktop/Raga/Code/Tonic_source_separation",i,"vocals.wav")
    command= "python3 main.py --path '" +  song +"'"
    os.system(command)
    print("HIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")
    # print(command)


