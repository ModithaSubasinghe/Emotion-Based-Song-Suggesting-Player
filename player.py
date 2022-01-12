import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

from MediaStore import song_adder, music_db
from MediaStore.music_db import MusicDb
from FaceImage import image_emotion
from MediaStore.player_controller import playerController


def about_us():
    showinfo('About EmooPlayer', 'This is a music player build using Python Tkinter by @emoviss')


def quite():
    app.quit()


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # configure the root window
        self.title('Emotion Based Song Suggesting player')
        self.geometry('1000x1000')

        self.button = ttk.Button(self, text='Click Me')
        self.button['command'] = self.button_clicked
        self.button.pack()

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


        # button


    def button_clicked(self):
        showinfo(title='Information',
                 message='Hello, Tkinter!')


if __name__ == "__main__":
    app = App()
    app.mainloop()