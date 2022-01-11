from mutagen.mp3 import MP3
from pygame import mixer
import threading
import time
import os
from os import path
from pydub import AudioSegment
from tkinter import messagebox

paused = False


# This is use to control the actions of player
class playerController:
    mixer.init()  # initializing the mixer

    def show_details(self, play_song):
        file_data = os.path.splitext(play_song)
        if file_data[1] == '.mp3':
            audio = MP3(play_song)
            total_length = audio.info.length
        else:
            a = mixer.Sound(play_song)
            total_length = a.get_length()
        return total_length

    def createQueue(self, x):
        mixer.music.queue(x)

    # mixer.music.get_busy(): - Returns FALSE when we press the stop button (music stop playing)
    def checkBusy(self):
        return (mixer.music.get_busy())

    # play selected song
    def play_music(self, play_it):
        print("play")
        global paused
        global playing
        playing = play_it
        if paused:
            mixer.music.unpause()
            paused = False
            return ("resumed")
        else:
            print("try")
            self.stop_music()
            time.sleep(1)
            print("selected")
            mixer.music.load(play_it)
            mixer.music.play()
            return ("playing")

    # stop a song
    def stop_music(self):
        print("stop")
        mixer.music.stop()
        return "                   Music Stopped"

    # Pause a song
    def pause_music(self):
        print("paused")
        global paused
        paused = True
        mixer.music.pause()
        return "                 Music Paused"

    # rewind a song
    def rewind_music(self):
        self.play_music(playing)
        print("rewined")
        return "                  Music Rewinded"

    # control volume
    def set_vol(self, val):
        volume = float(val) / 100
        mixer.music.set_volume(volume)
        # set_volume of mixer takes value only from 0 to 1. Example - 0, 0.1,0.55,0.54.0.99,1

    global muted
    muted = False

    # mute the player
    def mute_music(self):
        global muted
        if muted:  # Unmute the music
            mixer.music.set_volume(0.7)
            muted = False
            return "unmuted"
        else:  # mute the music
            mixer.music.set_volume(0)
            muted = True
            return "muted"