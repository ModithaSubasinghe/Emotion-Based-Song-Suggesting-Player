import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import os
import threading
import time
import os
from os import path
import matplotlib.pyplot as plt
# from PIL import Image
import pathlib

from MediaStore import song_adder
from MediaStore.music_db import MusicDb
from FaceImage import image_emotion
from MediaStore.player_controller import playerController

LARGE_FONT = ("Verdana", 12)


# show aboutus
def about_us():
    messagebox.showinfo('About EmooPlayer', 'This is a music player build using Python Tkinter by @emoviss')


def quite():
    app.quit()


# MAin windowAPP
class MusicPlayer(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Emotion Based Song Suggester")
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Add Song", command=lambda: song_adder.addSongs(musicdb))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quite)
        menubar.add_cascade(label="File", menu=filemenu)

        tk.Tk.config(self, menu=menubar)
        self.frames = {}
        global PlayerWindow
        for f in (StartPage, ViewerWindow, PlayerWindow):
            frame = f(container, self, musicdb)

            self.frames[f] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        viewmenu = tk.Menu(menubar, tearoff=1)
        startPage = StartPage(container, self, musicdb)
        viewmenu.add_command(label="View Songs", command=self.redirect)
        viewmenu.add_separator()
        viewmenu.add_command(label="About Us", command=about_us)
        menubar.add_cascade(label="View", menu=viewmenu)
        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.configure(background="black")
        frame.tkraise()

    def redirect(self):
        command = lambda: self.show_frame(ViewerWindow)
        command()


# this is the start Page
class StartPage(tk.Frame):
    def __init__(self, parent, controller, musicdb):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.musicdb = musicdb
        logo = tk.PhotoImage(file="images/background3.gif")
        BGlabel = tk.Label(self, image=logo)
        BGlabel.image = logo
        BGlabel.place(x=0, y=0)

        but1 = Button(self, padx=5, pady=5, width=39, bg='white', fg='black', relief=GROOVE, command=self.getImage,
                      text='Open Cam', font=('helvetica 15 bold'))
        but1.place(x=120, y=100)
        addButton = tk.Button(self, text=" TAKE PHOTO ", fg='red', font=24, command=self.getImage)

        label1 = tk.Label(self, text="\n\nWelcome to the Emo player\nPlay songs which fix yoyr mood ", fg='green',
                          font="Times 24")
        label2 = tk.Label(self, text="\n\nClick on TAKE PHOTO")

    # Resize the image
    def resize_image(event):
        new_width = event.width
        new_height = event.height
        image = copy_of_image.resize((new_width, new_height))
        photo = ImageTk.PhotoImage(image)
        label.config(image=photo)
        label.image = photo  # avoid garbage collection

    # Get real time face image
    def getImage(self):
        import numpy as np
        import cv2

        cap = cv2.VideoCapture(0)
        count = 0

        while (count != 1):
            # Capture frame-by-frame
            ret, frame = cap.read()

            # Our operations on the frame come here
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Display the resulting frame
            cv2.imwrite('images/frame.png', frame)
            count += 1
            '''
            if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            '''
            # When everything done, release the capture
            cap.release()
            cv2.destroyAllWindows()
            self.showImage()
            global emotion
            # emotion= "happiness"
            # Get emotion type from image through API
            emotion = faceEmotion.checkEmotion()
            f = open("faceimage/emotion.txt", "w")
            f.write(emotion)
            # If face is not detected print that
            if emotion == " ":
                lbl3 = Label(self, padx=5, width=100, bg="dim gray", fg='white', relief=GROOVE,
                             text="\n\nNO face Detected. Try Again!!", font=('helvetica 15 bold'))
                lbl3.place(x=20, y=500, relx=0.5, anchor=CENTER)
            # IF Face is detected show emotion type
            else:
                lbl3 = Label(self, padx=5, width=100, bg="dim gray", fg='red', relief=GROOVE,
                             text="\n\nYour current emotion :  " + emotion, font=('helvetica 15 bold'))
                lbl3.place(x=20, y=500, relx=0.5, anchor=CENTER)

                but3 = Button(self, padx=5, pady=5, width=39, fg='black', relief=GROOVE, text='Generate Playlist ',
                              command=lambda: self.controller.show_frame(PlayerWindow), font=('helvetica 15 bold'))
                but3.place(x=120, y=550)

    # show the obtained image from webcam
    def showImage(self):
        load = Image.open("images/frame.png")
        load = load.resize((250, 250), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(load)
        img = Label(self, image=render)
        img.image = render
        img.place(x=170, y=180)

    def redirect(self):
        command = lambda: self.controller.show_frame(ViewerWindow)
        command()


playlist = []
paused = FALSE


# This is the window that display songs which already added to the player
class ViewerWindow(tk.Frame):
    def __init__(self, parent, controller, musicdb):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.musicdb = musicdb
        logo = tk.PhotoImage(file="images/background3.gif")
        BGlabel = tk.Label(self, image=logo)
        BGlabel.image = logo
        BGlabel.place(x=0, y=0)
        but1 = Button(self, padx=5, pady=5, width=10, fg='black', relief=GROOVE, command=lambda: self.viewSong("all"),
                      text='All Songs ', font=('helvetica 15'))
        but1.place(x=50, y=104)
        but2 = Button(self, padx=5, pady=5, width=10, fg='black', relief=GROOVE, command=lambda: self.viewSong("happy"),
                      text='Happy Songs', font=('helvetica 15 bold'))
        but2.place(x=200, y=104)
        but3 = Button(self, padx=5, pady=5, width=10, fg='black', relief=GROOVE, command=lambda: self.viewSong("sad"),
                      text='Sad Songs', font=('helvetica 15 bold'))
        but3.place(x=350, y=104)
        but4 = Button(self, padx=5, pady=5, width=10, fg='black', relief=GROOVE, command=lambda: self.viewSong("calm"),
                      text='Calm Songs', font=('helvetica 15 bold'))
        but4.place(x=500, y=104)

        # view songlist inthe player

    def viewSong(self, emotiontype):
        global playlistbox
        playlistbox = Listbox(self, width=40, height=30, bg='ivory3', font=("Helvetica", 12))
        playlistbox.place(x=10, y=150)
        scrollbar = Scrollbar(self, orient="vertical")
        scrollbar.config(command=playlistbox.yview)
        playlistbox.config(yscrollcommand=scrollbar.set)

        # select required type by the user
        if emotiontype == "all":
            myresult = self.musicdb.getallsongs()
        if emotiontype == "happy":
            myresult = self.musicdb.getsongsforHappy()
        if emotiontype == "sad":
            myresult = self.musicdb.getsongsforSad()
        if emotiontype == "calm":
            myresult = self.musicdb.getsongsforCalm()
        print(myresult)
        for x in myresult:
            playercontroller.createQueue(x[0])
            filename = os.path.basename(x[0])
            index = 0
            playlistbox.insert(index, filename)
            playlist.insert(index, x[0])
            index += 1
        global lengthlabel
        lengthlabel = Label(self, text='Total Length : --:--')
        lengthlabel.place(x=380, y=200)
        global currenttimelabel
        currenttimelabel = Label(self, text='Current Time : --:--', relief=GROOVE)
        currenttimelabel.place(x=380, y=250)

        global playPhoto
        playPhoto = PhotoImage(file='images/play.png')
        playBtn = tk.Button(self, image=playPhoto, command=self.play_music)
        playBtn.place(x=380, y=300)
        global stopPhoto
        stopPhoto = PhotoImage(file='images/stop.png')
        stopBtn = tk.Button(self, image=stopPhoto, command=self.stop_music)
        stopBtn.place(x=480, y=300)
        global pausePhoto
        pausePhoto = PhotoImage(file='images/pause.png')
        pauseBtn = tk.Button(self, image=pausePhoto, command=self.pause_music)
        pauseBtn.place(x=580, y=300)
        global statusbar
        statusbar = ttk.Label(self, text="Welcome to Emoo Music", relief=SUNKEN, width=720, anchor=W,
                              font='Times 10 italic')
        statusbar.pack(side=BOTTOM, fill=X)
        statusbar.place(y=585)
        print(playlist)
        global rewindPhoto
        global rewindBtn
        rewindPhoto = PhotoImage(file='images/rewind.png')
        rewindBtn = Button(self, image=rewindPhoto, command=self.rewind_music)
        rewindBtn.place(x=400, y=400)
        global mutePhoto
        global volumePhoto
        global volumeBtn
        mutePhoto = PhotoImage(file='images/mute.png')
        volumePhoto = PhotoImage(file='images/volume.png')
        volumeBtn = Button(self, image=volumePhoto, command=self.mute_music)
        volumeBtn.place(x=450, y=400)
        global scale

        scale = Scale(self, from_=0, to=100, orient=HORIZONTAL, command=self.set_vol)
        scale.set(70)  # implement the default value of scale when music player starts
        playercontroller.set_vol(0.7)
        scale.place(x=550, y=400)

        but5 = Button(self, padx=5, pady=5, width=20, fg='black', relief=GROOVE,
                      command=lambda: self.controller.show_frame(StartPage), text='Back To Home',
                      font=('helvetica 15 bold'))
        but5.place(x=500, y=500)

    global paused
    paused = False

    def play_music(self):
        try:
            selected_song = playlistbox.curselection()
            selected_song = int(selected_song[0])
            print("selected")
            play_it = playlist[selected_song]
            play = playercontroller.play_music(play_it)
            print(play)
            if play == "resumed":
                global paused
                paused = False
                statusbar['text'] = "                   Music Resumed"
            else:
                statusbar['text'] = "               Playing music" + ' - ' + os.path.basename(play_it)
                total_length = playercontroller.show_details(play_it)
                mins, secs = divmod(total_length, 60)
                mins = round(mins)
                secs = round(secs)
                timeformat = '{:02d}:{:02d}'.format(mins, secs)
                lengthlabel['text'] = "Total Length" + ' - ' + timeformat
                t1 = threading.Thread(target=self.start_count, args=(total_length,))
                t1.start()
        except:
            messagebox.showerror('File not found', 'Melody could not find the file. Please check again.')

    def stop_music(self):
        stop = playercontroller.stop_music()
        statusbar['text'] = stop

    def pause_music(self):
        global paused
        paused = True
        pause = playercontroller.pause_music()
        statusbar['text'] = pause

    def rewind_music(self):
        rewind = self.play_music()
        statusbar['text'] = rewind

    def set_vol(self, val):
        playercontroller.set_vol(val)

    def mute_music(self):
        mute = playercontroller.mute_music()
        if mute == "unmuted":  # Unmute the music
            volumeBtn.configure(image=volumePhoto)
            scale.set(70)
        else:  # mute the music
            volumeBtn.configure(image=mutePhoto)
            scale.set(0)

    def start_count(self, t):
        # mixer.music.get_busy(): - Returns FALSE when we press the stop button (music stop playing)
        # Continue - Ignores all of the statements below it. We check if music is paused or not.
        current_time = 0
        while current_time <= t and playercontroller.checkBusy():
            if paused:
                continue
            else:
                mins, secs = divmod(current_time, 60)
                mins = round(mins)
                secs = round(secs)
                timeformat = '{:02d}:{:02d}'.format(mins, secs)
                currenttimelabel['text'] = "Current Time" + ' - ' + timeformat
                time.sleep(1)
                current_time += 1


# This is the window that shows after taken the face image
class PlayerWindow(tk.Frame):
    def __init__(self, parent, controller, musicdb):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.musicdb = musicdb
        logo = tk.PhotoImage(file="images/background3.gif")
        BGlabel = tk.Label(self, image=logo)
        BGlabel.image = logo
        BGlabel.place(x=0, y=0)
        lbl1 = Label(self, padx=5, width=100, bg="dim gray", fg='white', relief=GROOVE,
                     text="\n\nWe are genrating playlist according to your detected emotion type",
                     font=('helvetica 15 bold'))
        lbl1.place(x=20, y=130, relx=0.5, anchor=CENTER)
        but1 = Button(self, padx=5, pady=5, width=10, bg='white', fg='black', relief=GROOVE, command=self.continuee,
                      text='Continue', font=('helvetica 15 bold'))
        but1.place(x=120, y=180)
        but2 = Button(self, padx=5, pady=5, width=10, bg='white', fg='black', relief=GROOVE, text='Back',
                      command=self.clear, font=('helvetica 15 bold'))
        but2.place(x=420, y=180)

    global count
    count = 0

    def continuee(self):
        global count
        if count == 0:
            self.showPlaylist()
        else:
            playercontroller.stop_music()
            currenttimelabel['text'] = "00:00"
            self.showPlaylist()
        count += 1

    def clear(self):
        print("clear")
        playlistbox.place_forget()
        # scrollbar.place_forget()
        # statusbar.place_forget()
        # lengthlabel.place_forget()
        # currenttimelabel.place_forget()
        # playBtn.place_forget()
        # stopBtn.place_forget()
        # pauseBtn.place_forget()
        # rewindBtn.place_forget()
        # volumeBtn.place_forget()
        # scale.place_forget()
        self.controller.show_frame(StartPage)

    def showPlaylist(self):
        global playlistbox
        playlistbox = Listbox(self, width=40, height=30, bg='ivory3', font=("Helvetica", 12))
        playlistbox.place(x=10, y=180)
        scrollbar = Scrollbar(self, orient="vertical")
        scrollbar.config(command=playlistbox.yview)
        playlistbox.config(yscrollcommand=scrollbar.set)
        global statusbar
        statusbar = ttk.Label(self, text="Welcome to Emoo Music", relief=SUNKEN, width=720, anchor=W,
                              font='Times 10 italic')
        statusbar.pack(side=BOTTOM, fill=X)
        statusbar.place(y=585)
        f = open("faceimage/emotion.txt", "r")
        emotion = f.read()
        if emotion == "happiness":
            myresult1 = musicdb.getsongsforHappy()
        elif emotion == "sadness":
            myresult1 = musicdb.getsongsforSad()
        else:
            myresult1 = musicdb.getsongsforCalm()
        for x in myresult1:
            playercontroller.createQueue(x[0])
            filename = os.path.basename(x[0])
            index = 0
            playlistbox.insert(index, filename)
            playlist.insert(index, x[0])
            index += 1
        global lengthlabel
        lengthlabel = Label(self, text='Total Length : --:--')
        lengthlabel.place(x=380, y=250)
        global currenttimelabel
        currenttimelabel = Label(self, text='Current Time : --:--', relief=GROOVE)
        currenttimelabel.place(x=380, y=300)

        global playPhoto
        global playBtn
        playPhoto = PhotoImage(file='images/play.png')
        playBtn = tk.Button(self, image=playPhoto, command=self.play_music)
        playBtn.place(x=380, y=350)
        global stopPhoto
        global stopBtn
        stopPhoto = PhotoImage(file='images/stop.png')
        stopBtn = tk.Button(self, image=stopPhoto, command=self.stop_music)
        stopBtn.place(x=480, y=350)
        global pausePhoto
        global pauseBtn
        pausePhoto = PhotoImage(file='images/pause.png')
        pauseBtn = tk.Button(self, image=pausePhoto, command=self.pause_music)
        pauseBtn.place(x=580, y=350)
        print(playlist)
        global rewindPhoto
        global rewindBtn
        rewindPhoto = PhotoImage(file='images/rewind.png')
        rewindBtn = Button(self, image=rewindPhoto, command=self.rewind_music)
        rewindBtn.place(x=400, y=450)
        global mutePhoto
        global volumePhoto
        global volumeBtn
        mutePhoto = PhotoImage(file='images/mute.png')
        volumePhoto = PhotoImage(file='images/volume.png')
        volumeBtn = Button(self, image=volumePhoto, command=self.mute_music)
        volumeBtn.place(x=450, y=450)
        global scale
        scale = Scale(self, from_=0, to=100, orient=HORIZONTAL, command=self.set_vol)
        scale.set(70)  # implement the default value of scale when music player starts
        playercontroller.set_vol(0.7)
        scale.place(x=550, y=450)

    global paused
    paused = False

    def play_music(self):
        try:
            selected_song = playlistbox.curselection()
            selected_song = int(selected_song[0])
            print("selected")
            play_it = playlist[selected_song]
            play = playercontroller.play_music(play_it)
            print(play)
            if play == "resumed":
                global paused
                paused = False
                statusbar['text'] = "                   Music Resumed"
            else:
                statusbar['text'] = "      Playing music" + ' - ' + os.path.basename(play_it)
                total_length = playercontroller.show_details(play_it)
                mins, secs = divmod(total_length, 60)
                mins = round(mins)
                secs = round(secs)
                timeformat = '{:02d}:{:02d}'.format(mins, secs)
                lengthlabel['text'] = "Total Length" + ' - ' + timeformat
                t1 = threading.Thread(target=self.start_count, args=(total_length,))
                t1.start()
        except:
            messagebox.showerror('File not found', 'Melody could not find the file. Please check again.')

    def stop_music(self):
        stop = playercontroller.stop_music()
        statusbar['text'] = stop

    def pause_music(self):
        global paused
        paused = True
        pause = playercontroller.pause_music()
        statusbar['text'] = pause

    def rewind_music(self):
        rewind = self.play_music()
        statusbar['text'] = rewind

    def set_vol(self, val):
        playercontroller.set_vol(val)

    def mute_music(self):
        mute = playercontroller.mute_music()
        if mute == "unmuted":  # Unmute the music
            volumeBtn.configure(image=volumePhoto)
            scale.set(70)
        else:  # mute the music
            volumeBtn.configure(image=mutePhoto)
            scale.set(0)

    def start_count(self, t):
        # mixer.music.get_busy(): - Returns FALSE when we press the stop button (music stop playing)
        # Continue - Ignores all of the statements below it. We check if music is paused or not.
        current_time = 0
        while current_time <= t and playercontroller.checkBusy():
            if paused:
                continue
            else:
                mins, secs = divmod(current_time, 60)
                mins = round(mins)
                secs = round(secs)
                timeformat = '{:02d}:{:02d}'.format(mins, secs)
                currenttimelabel['text'] = "Current Time" + ' - ' + timeformat
                time.sleep(1)
                current_time += 1


musicdb = MusicDb()
musicdb.init()
app = MusicPlayer()
playercontroller = playerController()
app.geometry("720x600")
app.resizable(0, 0)
app.mainloop()
