import os
import tkinter as tk
from tkinter import *
import pygame
from tkinter import messagebox

from MediaStore import song_adder,music_db


# show aboutus
def about_us():
    messagebox.showinfo('About EmooPlayer', 'This is a music player build using Python Tkinter by @emoviss')


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
        filemenu.add_command(label="Add Song", command=lambda: song_adder.addSongs(music_db))
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



MusicPlayer.mainloop()


