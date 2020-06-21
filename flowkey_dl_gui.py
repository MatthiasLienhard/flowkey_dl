#!/bin/python3

from tkinter import *
import sys
from flowkey_dl import flowkey_dl, arange_image
import os
from PIL import ImageTk

class downloadWindow(object):
    def __init__(self,master):
        top=self.top=Toplevel(master)
        self.l=Label(top,text="Enter Download Link")
        self.l.pack()
        self.e = Entry(top)
        self.e.pack()
        self.b=Button(top,text='Download',command=self.download)
        self.b.pack()
    def download(self):
        url=self.e.get()
        self.image=flowkey_dl(url)
        self.top.destroy()

class mainWindow(object):
    def __init__(self,master):
        self.master=master
        self.b=Button(master,text="download",command=self.download)
        self.b.grid(row=0,column=0,rowspan=2)
        self.title_l=Label(master,text="Title")
        self.title_l.grid(row=0,column=1)
        self.title=Entry(master)
        self.title.grid(row=1,column=1)
        self.artist_l=Label(master,text="Artist/Author/Composer")
        self.artist_l.grid(row=0,column=2)
        self.artist=Entry(master)
        self.artist.grid(row=1,column=2)
        self.b2=Button(master,text="preview",command=self.arange_image)
        self.b2.grid(row=0,column=3, rowspan=2)
        self.scale = Scale(master, from_=10, to=200, orient=HORIZONTAL)
        self.scale.grid(row=2,column=0,columnspan=4)
        self.width=2480/4
        self.height=3508/4
        self.canvas = Canvas(master,width=self.width,height=self.height, bg='white') #100 dpi
        self.img=ImageTk.PhotoImage(arange_image(width=self.width, height=self.height))
        self.img_area=self.canvas.create_image(0,0,anchor=NW, image=self.img)
        self.canvas.grid(row=3,column=0,columnspan=4)

    def download(self):
        self.w=downloadWindow(self.master)
        self.b["state"] = "disabled" 
        self.master.wait_window(self.w.top)
        self.b["state"] = "normal"

    def arange_image(self):
        self.img=ImageTk.PhotoImage(arange_image(self.w.image, self.title.get(), self.artist.get(),self.width, self.height, scale=self.scale.get()/100))
        print('got an image!')
        #self.canvas.create_image(0,0,anchor=NW,image=ImageTk.PhotoImage(image))
        self.canvas.itemconfig(self.img_area, image = self.img)
       



if __name__ == "__main__":
    root=Tk()
    m=mainWindow(root)
    root.mainloop()