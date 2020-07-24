import librosa
import librosa.display
from swipe import *
# import swipe
from scipy import signal
import math
from collections import defaultdict, OrderedDict
import statistics
import copy
import os
import gc
import json
import parser
import argparse


parser = argparse.ArgumentParser(description='Paths to the song')
parser.add_argument('--path', help='path')
args = parser.parse_args()
# print(args.path)
songPath= args.path



plt.rcParams['figure.figsize'] = [20,5]
# defining the class 
# each object of this class is an audio clip that is to be analysed
class Audio:
  def __init__(self, path, sr=None, duration = None): 
    # loading the audio file
    self.x, self.sr1 = librosa.load(path= path, sr=sr,duration=duration)
    self.pitch_contour()
    self.constant_pitch()
    self.find_gamaka()
    self.find_stationary_points()
    self.develop_histogram(cpn = True)
    self.tonic = self.find_tonic()
    # self.normalize()
    # self.develop_histogram(cpn = False)
    # self.histogram()
    # self.find_all_notes()
    # self.sequence_notes = self.find_sequence_notes(self.all_notes)
    # self.pattern=self.find_pattern()
  # computing pitch contour
  def pitch_contour(self,dt = 0.01):
    self.pitch, self.time_axis, self.s = swipe(self.x,self.sr1,[100, 500],dt, 0.4)
    
  def constant_pitch(self ):
    
    time_axis_80 = []
    pitch_80 = []
    constant_pitch_time_80=[]
  
    for i in range(0,len(self.time_axis),8):
      pitch_80.append(self.pitch[i])
      time_axis_80.append(self.time_axis[i])
    delta = 12
      
    diff_80 = np.diff(pitch_80)

    for i in range(len(diff_80)):
      # constant note when the slope(of the pitch contour) is within the thershold i.e, delta =  
      if(diff_80[i]<delta/2 and diff_80[i]>-delta/2):
        constant_pitch_time_80.append(time_axis_80[i])
    self.constant_pitch_time_80 = np.array(constant_pitch_time_80)

    cpt = list(self.constant_pitch_time_80.round(2))
    tim = []
    initial = cpt[0]
    c= initial
    for i in range(1,len(cpt)):
      check = round(cpt[i]-c,2)
      if(check == 0.08):
        pass
      else:
        tim.append((initial,c))
        initial = cpt[i]
      if i == (len(cpt)-1):
        c= cpt[i]
        tim.append((initial,c))
      c= cpt[i]
    ta = list(self.time_axis)
    self.cpn_and_t = []
    for i in tim:
      begin = int(100*i[0])
      end = int(100*i[1])
      self.cpn_and_t.append((self.pitch[begin:end],ta[begin:end]))
    self.cpn_and_t = np.array(self.cpn_and_t)
    g,h = self.cpn_and_t.T
    self.cpn = np.array([item for sublist in g for item in sublist])
    self.cpt = np.array([item for sublist in h for item in sublist])
  
  def find_all_notes(self):  
    self.all_notes = []
    for i in self.n_pitch:
      if i in self.n_cpn or i in self.n_stp:
        self.all_notes.append(i)

  def find_gamaka(self):
    # deprecated
    def valid_gamaka(gamaka):
      valid_gamaka= []
      count = 0
      for j in gamaka:
        if math.isnan(j):
          count+=1
      if count <7:
        return True
      return False
    # --------------
    ta = list(self.time_axis)
    self.bt_cpn = []
    self.bt_cpt = []
    init = 0
    for _,j in self.cpn_and_t:
      if(j):
        begin = int(100*init)
        end = int(100*j[0])
        temp = self.pitch[begin:end]
        if(valid_gamaka(temp)):
          self.bt_cpn.append(temp)
          self.bt_cpt.append(ta[begin:end])
        init = j[-1]
  
  def find_stationary_points(self):
    self.stp = []
    self.stp_t = []
    for i in range(len(self.bt_cpn)):
      test = self.bt_cpn[i]
      test_time  = self.bt_cpt[i]
      for i in signal.find_peaks(test)[0]:
        self.stp.append(test[i])
        self.stp_t.append(test_time[i])
      for i in signal.find_peaks(-1*test)[0]:
        self.stp.append(test[i])
        self.stp_t.append(test_time[i])
  def develop_histogram(self,cpn):
    if(cpn):
      d = list(self.cpn) + list(self.stp)
      values=[x for x in d if (math.isnan(x) == False)]
      initial = 120
      end = 500
      increment = 1
      r = 0
    else:
      values = [x for x in self.n_pitch if (math.isnan(x) == False)]
      initial = all_normalized_notes['lSa0']
      end = all_normalized_notes['hNi3']
      increment = 0.01
      r = 2
    # values.extend(self.stp)
    values=[round(x,r) for x in values]
    occur=dict()
    self.d_hist=defaultdict(int)
    for i in values:
      if(i in occur):
        occur[i]+=1;
      else:
        occur[i]=1;
    j=initial
    while(j<=end):
      # print(j)
      if(j in occur):
        self.d_hist[j]=occur[j]
        # times.append(occur[j])
      else:
        self.d_hist[j]=0
      j+=increment
      j = round(j,r)

  def find_tonic(self):

    def close_5(arr):
      top5=list()
      for i in arr:
        count=0
        for j in arr:
          if(abs(i-j)<16):
            count+=1
        if (count>len(arr)/2):
          top5.append(i)
      return(top5)
    def toniclist(self) :
      un_notes=[]
      for i in list(self.cpn): 
        x=round(i)
        if(not(np.isnan(x))):
            un_notes.append(round(i,2))
      un_notes.sort()

      occur={}
      hist=defaultdict(int)
      for i in un_notes:
            if(i in occur):
              occur[i]+=1;
            else:
              occur[i]=1;
      # soccur = sorted(occur.items(), key=lambda x: x[1], reverse=True)
      # print("soccur :",soccur )
      # occurvalues=list(occur.values())
      #from collections import OrderedDict 
      # soccur = OrderedDict(sorted(occur.items()))
      soccur={k: v for k, v in sorted(occur.items(), key=lambda item: item[1],reverse=True)} 
      print("soccur :",soccur )
      occurvalues=list(occur.values())
      # occurvalues=[]
      # for i in soccur:
      #   occurvalues.append(i[0])
      # check signal.find_peaks
      indexlist=[]
      for i in range(1,len(occurvalues)-1):
        if((occurvalues[i-1]<occurvalues[i])and(occurvalues[i+1]<occurvalues[i])):
          indexlist.append(i)
      
      it=0
      toniclist=[]
      for i in occur:
        it+=1
        if(it in indexlist):
          # print(i," : ",occur[i])
          if(i>130):
            toniclist.append(i)
            # print(i," : ",occur[i])
      # after finding the peaks add stp to it
      return_toniclist=sorted(toniclist)
      return_toniclist=toniclist[:50]
      return(return_toniclist)
    
    def remove_outliers(an_array):
      if(len(an_array)<3):
        return(an_array)
      else:  
        mean=statistics.mean(an_array)
        an_array = np.array(an_array)
        # mean = np.mean(an_array)
        standard_deviation = np.std(an_array)
        distance_from_mean = abs(an_array - mean)
        max_deviations = 0.9
        not_outlier = distance_from_mean <= 1.1* max_deviations * standard_deviation
        no_outliers = an_array[not_outlier]

        return(no_outliers)
  
    def half_the_Sa(ton):

        if(ton>240):
          return (ton/2)
        else:
          return ton
    Sa_candidates=defaultdict(list)
    tonic_candidates=toniclist(self)
    Sa_tonic_candidates=[x for x in tonic_candidates if x>110 and x<240]
    print("Tonic candidates :",tonic_candidates)
    for i in tonic_candidates:
      for j in Sa_tonic_candidates :
            if(((i/j)>1.48) and ((i/j) <1.51)):
              Sa_candidates["Pa"].append(half_the_Sa(j))
            # if(((i/j)>1.06) and ((i/j) <1.067)):
            #   Sa_candidates["Ri1"].append(half_the_Sa(j))
            # if(((i/j)>1.19) and ((i/j) <1.21)):
            #   Sa_candidates["Ga2"].append(half_the_Sa(j))
              
            if(((i/j)>1.12) and ((i/j) <1.127) ):
              Sa_candidates["Ri2"].append(half_the_Sa(j))

            # if(((i/j)>1.4) and ((i/j) <1.42) ):
            #   Sa_candidates["Ma2"].append(half_the_Sa(j))
              
            # if(((i/j)>1.31) and ((i/j) <1.34) ):
            #   Sa_candidates["Ma1"].append(half_the_Sa(j))
              
            if(((i/j)>1.23) and ((i/j) <1.27)):
              Sa_candidates["Ga3"].append(half_the_Sa(j))
            # if(((i/j)>1.59) and ((i/j) <1.61)):
            #   Sa_candidates["Da1"].append(half_the_Sa(j))
              
            if(((i/j)>1.86) and ((i/j) <1.91) ):
              Sa_candidates["Ni3"].append(half_the_Sa(j))
            if(((i/j)>1.78) and ((i/j) <1.82) ):
              Sa_candidates["Ni2"].append(half_the_Sa(j))
            if(i>200):  
              if(((i/j)>1.98) and ((i/j) <2.2) ):
                Sa_candidates["High_Sa"].append(half_the_Sa(j))
            # check ratio with pa to high sa
            # songs at higher octave
            # if(j>200):
            #   #Pa
            #   if(((i/j)>0.74) and ((i/j) <0.76)):
            #     Sa_candidates["High_Sa"].append(half_the_Sa(j/2))
            #   #Da2
            #   if(((i/j)>0.82) and ((i/j) <0.85)):
            #     Sa_candidates["High_Sa"].append(half_the_Sa(j/2))
            #   #Ma
            #   if(((i/j)>0.65) and ((i/j) <0.68)):
            #     Sa_candidates["High_Sa"].append(half_the_Sa(j/2))
    # print("The Sa_candidates are : ",(Sa_candidates)) 

    for i in Sa_candidates:
      Sa_candidates[i]=remove_outliers(Sa_candidates[i])
    #   Sa_candidates[i]=close_5(Sa_candidates[i])

    if("Pa" in Sa_candidates):
      if(len(Sa_candidates["Pa"])!=0):
            Pa= mean(Sa_candidates["Pa"])
            if("High_Sa" in Sa_candidates):
              if(len(Sa_candidates["High_Sa"])!=0):

                      # if(Pa in Sa_candidates["High_Sa"]):
                      #   High_Sa=Pa
                      # else:
                        High_Sa = mean((Sa_candidates["High_Sa"]))
                        # print("x :",x)
                        # High_Sa=mean(x)

                        if(abs(High_Sa-Pa)<5 ):
                          #and (High_Sa+Pa) != 0
                              prob = High_Sa
                              print("SAPSPSAPSPASA")
                              return(half_the_Sa((prob+Pa)/2))     
                            
    
    for i in Sa_candidates:
      print("i :",i, " Sa_candidates[i] :", Sa_candidates[i])
        # print("i :",i, " Sa_candidates[i] :", Sa_candidates[i])
      if(len(Sa_candidates[i])!=0):
          Sa_candidates[i]=mean(Sa_candidates[i])
          
    

    temp=[i for i in list(Sa_candidates.values()) if(i)]
    # print("Temp :",temp)

    # temp2=remove_outliers(temp)
    # finallist=close_5(temp2)
    finallist=remove_outliers(temp)
    
    if(not(np.isnan(half_the_Sa(mean(finallist))))):
      print((half_the_Sa(mean(finallist))))
      return((half_the_Sa(mean(finallist))))

    else:
      print("Tonic not found")
  def histogram(self):
    self.hist_bins,self.hist_y = np.array(list(self.d_hist.items())).T
    self.n_hist_y = self.hist_y/len(self.pitch)

  def normalize(self):
    self.n_pitch = [12*np.log2(i/self.tonic) for i in self.pitch]
    # self.n_bt_cpn = [12*np.log2(j/self.tonic) for i in self.bt_cpn for j in i]
    self.n_bt_cpn = []
    for i in self.bt_cpn:
      self.n_bt_cpn.append([12*np.log2(j/self.tonic) for j in i])
    self.n_stp = [12*np.log2(i/self.tonic) for i in self.stp]
    self.n_cpn = [12*np.log2(i/self.tonic) for i in self.cpn]
  
  def find_sequence_notes(self,parameter):
    notes = []
    for k in parameter:
   
      if k in self.n_cpn:
        a = 0.04
      else:
        a = 0.135
      for i,j in all_normalized_notes.items():
        if (math.isclose(j,k,abs_tol= a)):
          notes.append(i)
    set_note = []
    initial = notes[0]
    set_note.append(initial)
    for i in range(1,len(notes)):
      if (initial != notes[i]):
        initial = notes[i]
        set_note.append(initial)
    return set_note
  def find_pattern(self):
    def countme(l,sl):
      count =0
      for i in range(0,len(l)):
        a=l[i:i+len(sl)]
        if (a==sl):
          count+=1
      return(count)
    cnt=0
    pattern=dict()
    for sublen in range(3,int(4)):
      for i in range(0,len(self.sequence_notes)-sublen):
        sub = self.sequence_notes[i:i+sublen]
        if(len(set(sub))>1):
          cnt = countme(self.sequence_notes,sub)
          str1=""
          strsub=str1.join(sub)
          if cnt >= (4) and strsub not in pattern:
            pattern[strsub] = cnt
    return pattern
  def plot(self,**kwargs):
    for key,value in kwargs.items():
      if(key=='contour' and value):
        plt.plot(self.time_axis,self.n_pitch,label = 'Pitch Contour')
      if(key == 'cpn' and value):
        plt.plot(self.time_axis,self.n_pitch,c="#FF0000",label = 'Pitch Contour')
        plt.scatter(self.cpt,self.n_cpn,c='0',label = 'Constant Pitch')
      if(key =='stp' and value):
        plt.scatter(self.stp_t,self.n_stp,c='#00FF00',label = 'Stationary Points')
        plt.plot(self.time_axis,self.n_pitch,c="#FF0000",label = 'Pitch Contour')
      if(key =='histogram' and value):
        plt.plot(self.hist_bins,  self.n_hist_y,label = "histogram")
      plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), shadow=True, ncol=2)


ratios = {'Sa0':1,'Ri1':16/15,'Ri2':9/8,'Ga2':6/5,'Ga3':5/4,'Ma1':4/3,'Ma2':17/12,'Pa0':3/2,'Da1':8/5,
          'Da2':5/3,'Ni2':9/5,'Ni3':15/8,'Sa2':2}
all_normalized_notes = dict()
for i,j in ratios.items():
  all_normalized_notes[i] = 12*np.log2(j)
  all_normalized_notes['l'+i] = 12*np.log2(0.5*j)
  all_normalized_notes['h'+i] = 12*np.log2(2*j)

del all_normalized_notes['lSa2']
del all_normalized_notes['hSa0']
all_normalized_notes = OrderedDict(sorted(all_normalized_notes.items(),key=lambda kv: kv[1]))

# rkm_kalyani=Audio('/home/kodhandarama/Desktop/Raga/Code/accompaniment.wav')


ourTonic ={}

# all_songs = os.listdir("/home/kodhandarama/Desktop/Raga/Code/Tonic_source_separation")
# all_songs.remove('.ipynb_checkpoints')
# all_songs.sort()
# path = "/home/kodhandarama/Desktop/Raga/Code/Tonic_source_separation/{songname}/vocals.wav"
f= open("/home/kodhandarama/Desktop/Raga/Code/compMusicDetails.json",)
compMusicTonicDetails = json.load(f)
f.close()
# for i in all_songs:
print("song ",os.path.basename(songPath))
with open("tempp.txt","a") as finished_file:
    finished_file.write(i+'\n')
song_to_test = Audio(songPath)
for j in compMusicTonicDetails:
    try:
        a=songPath.split('/home/kodhandarama/Desktop/Raga/Code/Tonic_source_separation/')[1]
        song_name=a.split('/vocals.wav')[0]
        # print("song_name : ",song_name)

        if compMusicTonicDetails[j]["songname"].split(".mp3")[0] == song_name:
            ourTonic[j] = compMusicTonicDetails[j]
            ourTonic[j]["Our Tonic"] = song_to_test.tonic
            json_object = json.dumps(ourTonic,indent = 4)
            with open("/home/kodhandarama/Desktop/Raga/Code/Result1.json", "a") as out:
                out.write(json_object) 
        
    except (KeyError, FileNotFoundError):
        pass
    # del song_to_test
    gc.collect()




