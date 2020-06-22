#!/bin/python3

from tkinter import *
from tkinter import ttk
import sys
from flowkey_dl import flowkey_dl, arange_image
import os
from PIL import ImageTk

dim={'A4 Landscape':(1169,826),'A4 Portrait':(826,1169)}

    
class MainWindow(object):
    def __init__(self,master):
        self.master=master
        self.song=Frame(master)
        self.song.grid(row=0,column=0)
        self.layout=Frame(master)
        self.layout.grid(row=1,column=0)
        self.measure=Frame(master)
        self.measure.grid(row=2, column=0)
        self.preview=Frame(master)
        self.preview.grid(row=0,column=1,rowspan=3)
        song=self.song
        self.song_lab=Label(song, text='Song:')
        self.song_lab.grid(row=0,column=0)
        self.title_l=Label(song,text="Title")
        self.title_l.grid(row=1,column=0)
        self.title=Entry(song)
        self.title.grid(row=1,column=1,columnspan=2)
        self.artist_l=Label(song,text="Artist/Author/Composer")
        self.artist_l.grid(row=2,column=0)
        self.artist=Entry(song)
        self.artist.grid(row=2,column=1,columnspan=2)
        self.url_l=Label(song,text="url")
        self.url_l.grid(row=3,column=0)
        self.url=Entry(song)
        self.url.grid(row=3,column=1,columnspan=2)
        self.download_b=Button(song,text="download",command=self.download)
        self.download_b.grid(row=4,column=0)
        self.load_b=Button(song,text="load",command=self.load)
        self.load_b.grid(row=4,column=1)
        self.save_b=Button(song,text="save",command=self.save)
        self.save_b.grid(row=4,column=2)
        layout=self.layout
        self.layout_lab=Label(layout, text='Layout:')
        self.layout_lab.grid(row=0, column=0)
        self.size_lab=Label(layout, text='Page size')
        self.size_lab.grid(row=1, column=0)
        self.size=ttk.Combobox(layout,state='readonly', values=list(dim))
        self.size.set('A4 Portrait')
        self.size.grid(row=1,column=1, columnspan=2)
        self.width,self.height=dim[self.size.get()]        
        self.scale_lab=Label(layout, text='sheet scale')
        self.scale_lab.grid(row=2,column=0)
        self.scale = Scale(layout, from_=10, to=200, orient=HORIZONTAL)
        self.scale.set(100)
        self.scale.grid(row=2,column=1,columnspan=2)
        self.prev_scale_lab=Label(layout, text='preview scale')
        self.prev_scale_lab.grid(row=3,column=0)
        self.prev_scale = Scale(layout, from_=10, to=100, orient=HORIZONTAL)
        self.prev_scale.set(50)
        self.prev_scale.grid(row=3,column=1,columnspan=2)   
        self.prev_width=self.width*self.prev_scale.get()/100     
        self.prev_height=self.height*self.prev_scale.get()/100     
        self.font_sz_lab=Label(layout, text='Font size')
        self.font_sz_lab.grid(row=4,column=0)
        self.font_sz_title=ttk.Combobox(layout,state='readonly', values=list(range(10,100)))
        self.font_sz_title.set(50)
        self.font_sz_title.grid(row=4,column=1)
        self.font_sz_author=ttk.Combobox(layout,state='readonly', values=list(range(10,100)))
        self.font_sz_author.set(30)
        self.font_sz_author.grid(row=4,column=2)
        self.space_lab=Label(layout,text='Spacing')
        self.space_lab.grid(row=5, column=0)
        self.space=Scale(layout, from_=10, to=200, orient=HORIZONTAL)
        self.space.set(50)
        self.space.grid(row=5,column=1, columnspan=2)
        measure=self.measure
        self.measure_lab=Label(measure, text='Measure')
        self.measure_lab.grid(row=0,column=0, columnspan=2)
        self.measure_sel_lab=Label(measure, text='select')
        self.measure_sel_lab.grid(row=1,column=0)
        self.measure_sel=Entry(measure)
        self.measure_sel.grid(row=1,column=1)
        self.measure_pre_lab=Label(measure, text='prevent break')
        self.measure_pre_lab.grid(row=2,column=0)
        self.measure_pre=Entry(measure)
        self.measure_pre.grid(row=2,column=1)
        self.measure_force_lab=Label(measure, text='force break')
        self.measure_force_lab.grid(row=3,column=0)
        self.measure_force=Entry(measure)
        self.measure_force.grid(row=3,column=1)
        preview=self.preview
        self.image=None
        self.current_page=0
        self.canvas = Canvas(preview,width=self.prev_width,height=self.prev_height, bg='white') #100 dpi
        self.prev_img=[ImageTk.PhotoImage(i) for i in arange_image(width=self.prev_width, height=self.prev_height)]
        self.prev_area=self.canvas.create_image(0,0,anchor=NW, image=self.prev_img[self.current_page])
        self.canvas.grid(row=0,column=0, columnspan=3)
        self.pre_b=Button(preview, text='<',command=self.pre_img)
        self.pre_b.grid(row=1, column=0)
        self.preview_lab=Label(preview, text=f'Page {self.current_page}/{len(self.prev_img)}')
        self.preview_lab.grid(row=1,column=1)
        self.next_b=Button(preview, text='>',command=self.next_img)
        self.next_b.grid(row=1, column=2)

    
    def download(self):
        url=self.url.get()
        self.image=flowkey_dl(url)
        self.get_preview()

    def save(self):
        print('not implemented yet... instead we make new preview')
        self.get_preview()
        
    def load(self):        
        pass

    def pre_img(self):
        self.current_page-=1
        self.preview_lab.config(text=f'Page {self.current_page}/{len(self.prev_img)}')
        self.canvas.itemconfig(self.prev_area, image = self.prev_img[self.current_page])

    def next_img(self):
        self.current_page+=1
        self.preview_lab.config(text=f'Page {self.current_page}/{len(self.prev_img)}')
        self.canvas.itemconfig(self.prev_area, image = self.prev_img[self.current_page])

    def get_preview(self):
        self.width,self.height=dim[self.size.get()]     
        self.prev_width=int(self.width*self.prev_scale.get()/100     )
        self.prev_height=int(self.height*self.prev_scale.get()/100     )
        self.canvas.config(width=self.prev_width, height=self.prev_height)
        self.prev_img=[ImageTk.PhotoImage(i.resize((self.prev_width, self.prev_height))) for i in arange_image(self.image, 
                            self.title.get(), self.artist.get(),self.width, self.height, 
                            scale=self.scale.get()/100,
                            space=int(self.space.get()),
                            sel_measures=self.measure_sel.get(), 
                            break_measures=self.measure_force.get(), 
                            nobreak_measures= self.measure_pre.get() ,
                            font_size=(int(self.font_sz_title.get()),int(self.font_sz_author.get())))]
        #self.canvas.create_image(0,0,anchor=NW,image=ImageTk.PhotoImage(image))
        self.canvas.itemconfig(self.prev_area, image = self.prev_img[self.current_page])
       



if __name__ == "__main__":
    root=Tk()
    m=MainWindow(root)
    root.mainloop()