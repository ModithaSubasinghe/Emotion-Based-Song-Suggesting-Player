from tkinter import filedialog
from tkinter import messagebox
from pydub import AudioSegment
import os
from os import path
from Model import emotion_predictor
from MediaStore import music_db
import numpy as np

# Add songs to the palyer
def addSongs(music_db):
    songs = []
    file_path = filedialog.askopenfilenames(title="Select Songs", filetypes=(("Mp3 Files", "*.mp3"),))
    for i in file_path:
        k = file_path.index(i)
        print(file_path[k])
        songs.append(file_path[k])
        print(str(songs))
    # mycursor.execute("SELECT url FROM song")
    # myresult = mycursor.fetchall()

    for x in songs:
        base = os.path.basename(x)
        print("base=" + base)
        name = os.path.splitext(base)[0]
        print("name=" + name)
        name1 = os.path.dirname(x)
        print(name1)
        my_result = music_db.getSong(name)
        print(x)

        if len(my_result) > 0:
            print("Song Already Added Before!!!")
            # popupmsg("Song Already Added Before!!!")
            messagebox.showinfo('!', 'Song Already Added Before!!!')

        else:
            emotion = emotion_predictor.detectEmotion(x)
            # convert wav to mp3
            sound = AudioSegment.from_mp3(x)
            print(emotion)
            dst = name1 + "/" + name + ".wav"
            print(dst)
            sound.export(dst, format="wav")
            music_db.insertsong(dst, name, emotion)
            # popupmsg("Song successfully added")
            messagebox.showinfo('!', 'Song successfully added \n Detected Emotion= ' + emotion)


