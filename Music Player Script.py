from tkinter import *
from pygame import mixer
import tkinter.messagebox
from tkinter import filedialog
import os
from tkinter import ttk
from ttkthemes import themed_tk as tk

root = tk.ThemedTk()  # creates a window (short lived)
root.get_themes()
root.set_theme("plastik")
root.title("MyMix")
root.iconbitmap(r'favicon.ico')  # imports icon in .ico extension only

statusbar = ttk.Label(root, text="WELCOME TO MyMix", relief=SUNKEN, font='Courier 15 italic')
statusbar.pack(side=BOTTOM, fill=X)

leftframe = Frame(root)
leftframe.pack(side=LEFT, padx=30, pady=30)

rightframe = Frame(root)
rightframe.pack(pady=30)

topframe = Frame(rightframe)
topframe.pack()

middleframe = Frame(rightframe)
middleframe.pack(padx=10, pady=10)

bottomframe = Frame(rightframe)
bottomframe.pack()

mixer.init()  # initializing the mixer

def play_music():  # function to load and play music
    global paused
    if paused:
        mixer.music.unpause()  # unpauses the music when play button is clicked
        statusbar['text'] = "Music Resumed"
        paused = False
    else:
        try:
            stop_music()
            selected_song = playlist.curselection()  # selecting the current song to be played in the playlist
            selected_song = int(selected_song[0])  # returning the index of the song in the form of an integer
            play_it = playlist0[selected_song]  # using the hence found integer index of the song to play music
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar["text"] = 'Now Playing' + ' ' + os.path.basename(play_it)
        except:  # error handling when flie not selected
            tkinter.messagebox.showerror('FILE NOT FOUND', 'Please select valid file')


playphoto = PhotoImage(file=r'play.png')  # add the play icon
playbtn = ttk.Button(middleframe, image=playphoto, command=play_music)
playbtn.grid(row=0, column=1, padx=10)

paused = False


def pause_music():  # function to pause music
    global paused
    paused = TRUE  # pauses the music
    mixer.music.pause()
    statusbar["text"] = 'Paused Playing'


pausephoto = PhotoImage(file=r'pause.png')  # add the stop icon
pausebtn = ttk.Button(middleframe, image=pausephoto, command=pause_music)
pausebtn.grid(row=0, column=3, padx=10)


def stop_music():  # function to stop music
    mixer.music.stop()
    statusbar["text"] = 'Stopped Playing'


stopphoto = PhotoImage(file=r'stop.png')  # add the stop icon
stopbtn = ttk.Button(middleframe, image=stopphoto, command=stop_music)
stopbtn.grid(row=0, column=2, padx=10)


def set_vol(val):  # function to set volume
    volume = float(val) / 100  # val takes values only between 1 and 0
    mixer.music.set_volume(volume)


scale = ttk.Scale(root, from_=0, to=100, orient=HORIZONTAL, command=set_vol)  # volume adjustment
scale.set(50)  # giving a default value to volume button
mixer.music.set_volume(0.5)
scale.pack(pady=10)

muted = False


def mute_music():
    global muted
    global last_volume
    if muted:
        mixer.music.set_volume(0.5)
        mutebtn.configure(image=volumephoto)
        scale.set(50)
        muted = False
    else:
        mixer.music.set_volume(0)
        mutebtn.configure(image=mutephoto)
        scale.set(0)
        muted = True


mutephoto = PhotoImage(file=r'mute.png')  # add the mute icon
volumephoto = PhotoImage(file=r'speaker.png')
mutebtn = ttk.Button(bottomframe, image=volumephoto, command=mute_music)
mutebtn.grid(row=0, column=2, padx=10)

menubar = Menu(root)  # create menubar
root.config(menu=menubar)


def browse_file():  # search for files
    global filename_path
    filename_path = filedialog.askopenfilename()
    add_to_playlist(filename_path)


submenu = Menu(menubar, tearoff=0)  # create the submenu
menubar.add_cascade(label="FILE", menu=submenu)
submenu.add_command(label="Search songs", command=browse_file)


def about_programmer():
    tkinter.messagebox.showinfo('About the programmer','Programmer Name:Farhaan Areeb\nReg.No.:21BCE1500\nCourse Code: BCSE103N')


submenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="HELP", menu=submenu)
submenu.add_command(label="about programmer", command=about_programmer)

submenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="EXIT", command=root.destroy)

playlist0 = []  # contains the full path and filename
playlist = Listbox(leftframe)  # contains only filename
playlist.pack()

def add_to_playlist(filename):  # create a playlist
    filename = os.path.basename(filename)
    index = 0
    playlist.insert(index, filename)
    playlist0.insert(index, filename_path)
    playlist.pack()
    index += 1

addbtn = ttk.Button(leftframe, text="+ADD", command=browse_file)  # create add and delete button for playlist
addbtn.pack(side=LEFT)

def del_song():  # delete songs fom playlist
    selected_song = playlist.curselection()
    selected_song = int(selected_song[0])
    playlist.delete(selected_song)
    playlist0.pop()  # removing items from the list, playlist0 to avoid pileup(good practice)

deletebtn = ttk.Button(leftframe, text="-DELETE", command=del_song)
deletebtn.pack(side=LEFT)

root.mainloop()  # looping the window hence created