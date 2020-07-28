import os
import json
five_candidates=[]
ten_candidates=[]
not_working = []
missed=0
# all_songs = os.listdir("/home/kodhandarama/Desktop/Raga/Code/Audio_Analysis/lolol")
all_songs = os.listdir("/home/darth_kronos/Desktop/tonic/")
# all_songs.remove('.ipynb_checkpoints')
all_songs.sort()
for i in all_songs:
	command= "python3 main.py --song '" +  i + "'" 
	os.system(command)
	tonic_file = open('our_tonic_v04.json','r')
	data = json.load(tonic_file)
	tonic_file.close()
	for j in data :
		song = data[j]
		if data[j]["songname"].split(".mp3")[0] == i:
			print(song['Tonic'])
			if (abs(song['Tonic']-song['Our Tonic'])<=5):
				five_candidates.append(i)
			elif(abs(song['Tonic']-song['Our Tonic']))<=10:
				not_working.append(i)
				ten_candidates.append(i)
			else:
				not_working.append(i)
				missed +=1

print(five_candidates)
print(not_working)
print(len(five_candidates))
print(len(not_working))