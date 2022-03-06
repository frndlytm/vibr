import subprocess
import pandas as pd
import re
import pickle

metadata = "../data/listening-moods/metadata_short.csv"
df = pd.read_csv(metadata)
# print(df.head())
allmusic_root = "https://www.allmusic.com/search/all/"

song_to_mood = {}

for idx, row in df.iterrows():
    
    # print(subprocess.run("pwd"))
    # print("wget " +  allmusic_root + "\'" + row.track_name + "\'" +  " -O ../data/allmusic/search/" + row.song_id + ".txt ")
    subprocess.run("wget -q " +  allmusic_root + "\'" + row.track_name + "\'" +  " -O ../data/allmusic/search/" + row.song_id + ".txt ", shell=True)
    target_mood=[]
    with open("../data/allmusic/search/" + row.song_id + ".txt", "r") as f:
        for line in f:
            
            if "<h4>Song</h4>" in line:
                print(row.track_name)
                next(f)
                next(f)
                song_url = next(f).split('"')[1]
                subprocess.run("wget -q " +  song_url + "/attributes -O ../data/allmusic/song/" + row.song_id + ".txt", shell=True)
                
                with open("../data/allmusic/song/" + row.song_id + ".txt", "r") as h:
                    
                    for l in h:
                        if 'title="All Moods"' in l:
                            
                            next(h)
                            next(h)
                            next(h)
                            mood = next(h)
                            while "</div>" not in mood:
                                
                                mood = re.split('"|/', mood)[3]
                                target_mood.append(mood)
                                mood = next(h)
                            break
                break
    song_to_mood[row.song_id] = target_mood

pickle.dump(song_to_mood, open("../data/allmusic/mood.pkl", "wb"))

# with open('output2.txt', 'w') as f:
#         f.write(str(html))