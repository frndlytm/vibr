import csv
import numpy as np
import jsonlines


def merge_moods():

    album_data = "data/raw/albums.jl"
    meta_data = "data/listening_moods_data/metadata.csv"
    mood_labels = "data/listening_moods_data/moods.txt"

    #set up dictionary mapping foreach album to its moods
    album_and_moods = {}
    with jsonlines.open(album_data) as reader:
        for obj in reader:
            album_name = ""
            album_moods = []
            for key, val in obj.items():
                if(key == "moods"):
                    album_moods = val
                if(key == "title"):
                    album_name = val.strip()
            album_and_moods[album_name] = album_moods

    #Test - moods data is currentlyempty so fill out one to try out
    album_and_moods['The Greatest Songs Ever Written'] = ['Animated','Dramatic', 'Effervescent']
    #indexes: 8, 41, 49

    #create a dictionary mapping of each mood to an index in order of moods.txt
    moods_dict = {}
    index = 0
    moods_classes = open(mood_labels)
    for line in moods_classes:
        moods_dict[line.strip()] = index
        index += 1

    #map a moods vector to each song id based its album's moods
    song_id_to_moods = []
    with open(meta_data, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)  # skip the headers
        for row in reader:
            new_entry = []
            new_entry.append(row[2]) #add song id

            #get album moods
            moods_raw = get_moods(album_and_moods,row[5])
            if moods_raw is None:
                moods_encode = []
            else:
                moods_encode = moods_to_array(moods_dict,moods_raw)
            new_entry.append(moods_encode)

            song_id_to_moods.append(new_entry)


    #save an numpy array
    song_id_to_moods = np.array(song_id_to_moods, dtype=object)
    print(song_id_to_moods[0])
    np.save('data/moods_target.npy', song_id_to_moods, allow_pickle=True, fix_imports=True)


def get_moods(album_and_moods, album_name):
    """
    get the moods for an album
    """
    try:
        return album_and_moods[album_name]
    except:
       return None

def moods_to_array(moods_dict, example_moods):
    """
    convert list of moods from moods.txt into a one hot
    encoded array for every possible mood
    """
    out = [0 for i in range(len(moods_dict.keys()))]
    for ex in example_moods:
        index = None
        try:
            index = moods_dict[ex]
        except:
            Exception("invlaid mood value: ", ex)
            return None
        out[index] = 1

    return out


if __name__=="__main__":
    merge_moods()