import subprocess
import pandas as pd
import re
import pickle

metadata = "../data/listening-moods/metadata.csv"
df = pd.read_csv(metadata)
allmusic_root = "https://www.allmusic.com/search/all/"

song_to_mood = {}
failed = []

for idx, row in df.iterrows():

    subprocess.run("wget -q " +  allmusic_root + "\'" + row.track_name + "\'" +  " -O ../data/allmusic/search/" + row.song_id + ".txt ", shell=True)
    target_mood=[]
    try:
        with open("../data/allmusic/search/" + row.song_id + ".txt", "r") as f:
            for line in f:
                
                if "<h4>Song</h4>" in line:
                    # print(row.track_name)
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

                                while "div" not in mood:
                                    mood = re.split('"|/', mood)[3]
                                    target_mood.append(mood)
                                    mood = next(h)
                                break
                    break
    except:
        failed.append(row.song_id)
    if len(target_mood) > 0:
        song_to_mood[row.song_id] = target_mood
pickle.dump(failed, open("../data/allmusic/failed.pkl", "wb"))
print("Success: ", str(len(song_to_mood)), "\t failed: ", str(len(failed)))

pickle.dump(song_to_mood, open("../data/allmusic/mood.pkl", "wb"))

# with open('output2.txt', 'w') as f:
#         f.write(str(html))