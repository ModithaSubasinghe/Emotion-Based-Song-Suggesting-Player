import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox

import threading
import time
import os
import cv2

from MediaStore import song_adder, music_db
from MediaStore.music_db import MusicDb
from FaceImage import image_emotion
from MediaStore.player_controller import playerController

LARGE_FONT = ("Verdana", 12)


# show aboutus
def about_us():
    messagebox.showinfo('About EmooPlayer', 'This is a music player build using Python Tkinter ')


def quite():
    app.quit()


# MAin windowAPP
class MusicPlayer(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Emotion Based Song Suggesting Player")
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Add Song", command=lambda: song_adder.addSongs(music_db))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quite)
        menubar.add_cascade(label="File", menu=filemenu)

        tk.Tk.config(self, menu=menubar)
        self.frames = {}
        global PlayerWindow
        for f in (StartPage, ViewerWindow, PlayerWindow):
            frame = f(container, self, music_db)

            self.frames[f] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        viewmenu = tk.Menu(menubar, tearoff=1)
        startPage = StartPage(container, self, music_db)
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
    def __init__(self, parent, controller, music_db):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.music_db = music_db
        logo = tk.PhotoImage(file="Images/emoo.png")
        BGlabel = tk.Label(self, image=logo)
        BGlabel.image = logo
        BGlabel.place(x=0, y=0)

        but1 = Button(self, padx=5, pady=5, width=15, bg='#0C0C0C', fg='#1DD3D0', activebackground='#E2F1F1', relief=GROOVE, command=self.getImage,
                      text='Open Cam', font=('helvetica 15 bold'))
        but1.place(x=400, y=200)



    # Get real time face image
    def getImage(self):
        cam = cv2.VideoCapture(0)
        count = 0
        while (count != 1):
            ret, img = cam.read()
            cv2.imshow("Press Space Button To Take A Photo", img)
            if not ret:
                break
            k = cv2.waitKey(1)

            if k % 256 == 27:
                print("close")
                break

            if k % 256 == 32:
                print("Image saved")
                cv2.imwrite('Images/image.jpg', img)
                count += 1
        cam.release()
        cv2.destroyAllWindows()
        self.showImage()
        global emotion
        emotion = str(image_emotion.checkEmotion())
        f = open("faceimage/emotion.txt", "w")
        f.write(emotion)

        # If face is not detected print that
        if emotion == "None":
            lbl3 = Label(self, padx=5, width=20, bg="dim gray", fg='white', relief=GROOVE,
                         text="NO face Detected\n Try Again!!", font=('helvetica 15 bold'))
            lbl3.place(x=140, y=540, anchor=CENTER)

            but3 = Button(self, padx=5, pady=5, width=15, fg='black', relief=GROOVE, text='Click again on\n Open cam',
                          command=lambda: self.controller.show_frame(StartPage), font=('helvetica 15 bold'))
            but3.place(x=760, y=475)

            # IF Face is detected show emotion type
        elif emotion == "neutral":
            emotion ="calm"
            lbl3 = Label(self, padx=5, width=20, bg="dim gray", fg='red', relief=GROOVE,
                         text="Your current emotion is \n" + emotion, font=('helvetica 15 bold'))
            lbl3.place(x=140, y=540,  anchor=CENTER)

            but3 = Button(self, padx=5, pady=5, width=15, fg='black', relief=GROOVE, text='Generate \nPlaylist ',
                          command=lambda: self.controller.show_frame(PlayerWindow), font=('helvetica 15 bold'))
            but3.place(x=760, y=475)

        elif emotion == "angry":
            lbl3 = Label(self, padx=5, width=20, bg="dim gray", fg='white', relief=GROOVE,
                         text="You have angry face.\n Try Again!!", font=('helvetica 15 bold'))
            lbl3.place(x=140, y=540, anchor=CENTER)

            but3 = Button(self, padx=5, pady=5, width=15, fg='black', relief=GROOVE, text='Click again on\n Open cam',
                          command=lambda: self.controller.show_frame(StartPage), font=('helvetica 15 bold'))
            but3.place(x=760, y=475)

        elif emotion == "fear":
            lbl3 = Label(self, padx=5, width=20, bg="dim gray", fg='white', relief=GROOVE,
                         text="You have fear face.\n Try Again!!", font=('helvetica 15 bold'))
            lbl3.place(x=140, y=540, anchor=CENTER)
            but3 = Button(self, padx=5, pady=5, width=15, fg='black', relief=GROOVE, text='Click again on\n Open cam',
                          command=lambda: self.controller.show_frame(StartPage), font=('helvetica 15 bold'))
            but3.place(x=760, y=475)

        elif emotion == "surprise":
            lbl3 = Label(self, padx=5, width=20, bg="dim gray", fg='white', relief=GROOVE,
                         text="You have surprise face.\n Try Again!!", font=('helvetica 15 bold'))
            lbl3.place(x=140, y=540, anchor=CENTER)
            but3 = Button(self, padx=5, pady=5, width=15, fg='black', relief=GROOVE, text='Click again on\n Open cam',
                          command=lambda: self.controller.show_frame(StartPage), font=('helvetica 15 bold'))
            but3.place(x=760, y=475)

        else:
            lbl3 = Label(self, padx=5, width=20, bg="dim gray", fg='red', relief=GROOVE,
                         text="Your current emotion is \n" + emotion, font=('helvetica 15 bold'))
            lbl3.place(x=140, y=540, anchor=CENTER)

            but3 = Button(self, padx=5, pady=5, width=15, fg='black', relief=GROOVE, text='Generate \nPlaylist ',
                          command=lambda: self.controller.show_frame(PlayerWindow), font=('helvetica 15 bold'))
            but3.place(x=760, y=475)

    # show the obtained image from webcam
    def showImage(self):
        load = Image.open("Images/image.jpg")
        load = load.resize((200, 200), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(load)
        img = Label(self, image=render)
        img.image = render
        img.place(x=50, y=300)

    def redirect(self):
        command = lambda: self.controller.show_frame(ViewerWindow)
        command()


playlist = []
paused = FALSE


# This is the window that display songs which already added to the player
class ViewerWindow(tk.Frame):
    def __init__(self, parent, controller, music_db):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.music_db = music_db
        logo = tk.PhotoImage(file="Images/Viewer Window.png")
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
        playlistbox = Listbox(self, width=40, height=20, bg='ivory3', font=("Helvetica", 12))
        playlistbox.place(x=10, y=200)
        scrollbar = Scrollbar(self, orient="vertical")
        scrollbar.config(command=playlistbox.yview)
        playlistbox.config(yscrollcommand=scrollbar.set)

        # select required type by the user
        if emotiontype == "all":
            myresult = self.music_db.getallsongs()
        if emotiontype == "happy":
            myresult = self.music_db.getsongsforHappy()
        if emotiontype == "sad":
            myresult = self.music_db.getsongsforSad()
        if emotiontype == "calm":
            myresult = self.music_db.getsongsforCalm()
        print(myresult)

        for x in myresult:

            filename = os.path.basename(x[0])
            index = 0
            playlistbox.insert(index, filename)
            playlist.insert(index, x[0])
            index += 1

        global lengthlabel
        lengthlabel = Label(self, text='Total Length : --:--',borderwidth=0, bg='#17ADAB')
        lengthlabel.place(x=380, y=200)
        global currenttimelabel
        currenttimelabel = Label(self, text='Current Time : --:--', relief=GROOVE, borderwidth=0, bg='#17ADAB')
        currenttimelabel.place(x=380, y=250)

        global playPhoto
        play_photo = Image.open('images/play.png')
        playPhoto = ImageTk.PhotoImage(play_photo.resize((40,40)))
        playBtn = tk.Button(self, image=playPhoto, command=self.play_music, borderwidth=0, bg='#0FADAE')
        playBtn.place(x=380, y=300)

        global stopPhoto
        stop_Photo = Image.open('images/stop.png')
        stopPhoto = ImageTk.PhotoImage(stop_Photo.resize((40,40)))
        stopBtn = tk.Button(self, image=stopPhoto, command=self.stop_music, borderwidth=0, bg='#0FADAE')
        stopBtn.place(x=380, y=360)

        global pausePhoto
        pause_Photo = Image.open('images/pause.png')
        pausePhoto = ImageTk.PhotoImage(pause_Photo.resize((40, 40)))
        pauseBtn = tk.Button(self, image=pausePhoto, command=self.pause_music, borderwidth=0, bg='#14B7B6')
        pauseBtn.place(x=440, y=300)

        global statusbar
        statusbar = ttk.Label(self, text="Welcome to Emoo Music", relief=SUNKEN, width=720, anchor=W,
                              font='Times 10 italic')
        statusbar.pack(side=BOTTOM, fill=X)
        statusbar.place(y=585)
        print(playlist)

        global rewindPhoto
        global rewindBtn
        rewind_Photo = Image.open('images/rewind.png')
        rewindPhoto = ImageTk.PhotoImage(rewind_Photo.resize((40, 40)))
        rewindBtn = Button(self, image=rewindPhoto, command=self.rewind_music,borderwidth=0, bg='#14B2B5')
        rewindBtn.place(x=440, y=360)

        global mutePhoto
        global volumePhoto
        global volumeBtn


        global scale
        scale = Scale(self, from_=0, to=100, orient=HORIZONTAL, command=self.set_vol, borderwidth=0, bg="#000000", fg="#20C5C9")
        scale.set(70)  # implement the default value of scale when music player starts
        player_controller.set_vol(0.7)
        scale.place(x=550, y=250)

        volume_label= Label(self, text="Volume", relief=SUNKEN, width=7, anchor=W, borderwidth=0,
                              font='Times 10 italic', bg="#20C5C9")
        volume_label.place(x=580, y=300)

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
            play = player_controller.play_music(play_it)
            print(play)
            if play == "resumed":
                global paused
                paused = False
                statusbar['text'] = "                   Music Resumed"
            else:
                statusbar['text'] = "               Playing music" + ' - ' + os.path.basename(play_it)
                total_length = player_controller.show_details(play_it)
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
        stop = player_controller.stop_music()
        statusbar['text'] = stop

    def pause_music(self):
        global paused
        paused = True
        pause = player_controller.pause_music()
        statusbar['text'] = pause

    def rewind_music(self):
        rewind = self.play_music()
        statusbar['text'] = rewind

    def set_vol(self, val):
        player_controller.set_vol(val)

    def mute_music(self):
        mute = player_controller.mute_music()
        if mute == "unmuted":  # Unmute the music
            volumeBtn.configure(image=volumePhoto)
            scale.set(70)
        else:  # mute the music
            volumeBtn.configure(image=mutePhoto)
            scale.set(0)

    def start_count(self, t):

        current_time = 0
        while current_time <= t and player_controller.checkBusy():
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
    def __init__(self, parent, controller, music_db):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.music_db = music_db
        logo = tk.PhotoImage(file="images/Viewer Window.png")
        BGlabel = tk.Label(self, image=logo)
        BGlabel.image = logo
        BGlabel.place(x=0, y=0)
        lbl1 = Label(self, padx=20, width=35, bg="dim gray", fg='white', relief=GROOVE,
                     text="We are genrating playlist according to \nyour detected emotion type",
                     font=('helvetica 15 bold'))
        lbl1.place(x=340, y=100, anchor=CENTER)
        but1 = Button(self, padx=5, pady=5, width=10, bg='white', fg='black', relief=GROOVE, command=self.continuee,
                      text='Continue', font=('helvetica 15 bold'))
        but1.place(x=120, y=180)
        # but2 = Button(self, padx=5, pady=5, width=10, bg='white', fg='black', relief=GROOVE, text='Back',
        #               command=self.clear, font=('helvetica 15 bold'))
        # but2.place(x=420, y=180)

    global count
    count = 0

    def continuee(self):
        global count
        if count == 0:
            self.showPlaylist()
        else:
            player_controller.stop_music()
            currenttimelabel['text'] = "00:00"
            self.showPlaylist()
        count += 1

    def clear(self):
        print("clear")
        playlistbox.place_forget()
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
        if emotion == "happy":
            myresult1 = music_db.getsongsforHappy()
        elif emotion == "sad":
            myresult1 = music_db.getsongsforSad()
        else:
            myresult1 = music_db.getsongsforCalm()
        for x in myresult1:
            filename = os.path.basename(x[0])
            index = 0
            playlistbox.insert(index, filename)
            playlist.insert(index, x[0])
            index += 1

        global lengthlabel
        lengthlabel = Label(self, text='Total Length : --:--', borderwidth=0, bg='#17ADAB')
        lengthlabel.place(x=380, y=200)
        global currenttimelabel
        currenttimelabel = Label(self, text='Current Time : --:--', relief=GROOVE, borderwidth=0, bg='#17ADAB')
        currenttimelabel.place(x=380, y=250)

        global playPhoto
        play_photo = Image.open('images/play.png')
        playPhoto = ImageTk.PhotoImage(play_photo.resize((40, 40)))
        playBtn = tk.Button(self, image=playPhoto, command=self.play_music, borderwidth=0, bg='#0FADAE')
        playBtn.place(x=380, y=300)

        global stopPhoto
        stop_Photo = Image.open('images/stop.png')
        stopPhoto = ImageTk.PhotoImage(stop_Photo.resize((40, 40)))
        stopBtn = tk.Button(self, image=stopPhoto, command=self.stop_music, borderwidth=0, bg='#0FADAE')
        stopBtn.place(x=380, y=360)

        global pausePhoto
        pause_Photo = Image.open('images/pause.png')
        pausePhoto = ImageTk.PhotoImage(pause_Photo.resize((40, 40)))
        pauseBtn = tk.Button(self, image=pausePhoto, command=self.pause_music, borderwidth=0, bg='#14B7B6')
        pauseBtn.place(x=440, y=300)

        # global statusbar
        # statusbar = ttk.Label(self, text="Welcome to Emoo Music", relief=SUNKEN, width=720, anchor=W,
        #                       font='Times 10 italic')
        # statusbar.pack(side=BOTTOM, fill=X)
        # statusbar.place(y=585)
        # print(playlist)

        global rewindPhoto
        global rewindBtn
        rewind_Photo = Image.open('images/rewind.png')
        rewindPhoto = ImageTk.PhotoImage(rewind_Photo.resize((40, 40)))
        rewindBtn = Button(self, image=rewindPhoto, command=self.rewind_music, borderwidth=0, bg='#14B2B5')
        rewindBtn.place(x=440, y=360)

        global mutePhoto
        global volumePhoto
        global volumeBtn

        global scale
        scale = Scale(self, from_=0, to=100, orient=HORIZONTAL, command=self.set_vol, borderwidth=0, bg="#000000",
                      fg="#20C5C9")
        scale.set(70)  # implement the default value of scale when music player starts
        player_controller.set_vol(0.7)
        scale.place(x=550, y=250)

        volume_label = Label(self, text="Volume", relief=SUNKEN, width=7, anchor=W, borderwidth=0,
                             font='Times 10 italic', bg="#20C5C9")
        volume_label.place(x=580, y=300)

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
            play = player_controller.play_music(play_it)
            print(play)
            if play == "resumed":
                global paused
                paused = False
                statusbar['text'] = "                   Music Resumed"
            else:
                statusbar['text'] = "      Playing music" + ' - ' + os.path.basename(play_it)
                total_length = player_controller.show_details(play_it)
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
        stop = player_controller.stop_music()
        statusbar['text'] = stop

    def pause_music(self):
        global paused
        paused = True
        pause = player_controller.pause_music()
        statusbar['text'] = pause

    def rewind_music(self):
        rewind = self.play_music()
        statusbar['text'] = rewind

    def set_vol(self, val):
        player_controller.set_vol(val)

    def mute_music(self):
        mute = player_controller.mute_music()
        if mute == "unmuted":  # Unmute the music
            volumeBtn.configure(image=volumePhoto)
            scale.set(70)
        else:  # mute the music
            volumeBtn.configure(image=mutePhoto)
            scale.set(0)

    def start_count(self, t):

        current_time = 0
        while current_time <= t and player_controller.checkBusy():
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


music_db = MusicDb()
music_db.init()
app = MusicPlayer()
player_controller = playerController()
app.geometry("1000x600")
app.resizable(0, 0)
app.mainloop()