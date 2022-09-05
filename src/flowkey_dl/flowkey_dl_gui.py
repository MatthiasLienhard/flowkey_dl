#!/bin/python3

from tkinter import Tk, ttk, filedialog
from tkinter import Button, Frame, Label, Scale, Entry, Canvas
from tkinter import HORIZONTAL, END, NW
from flowkey_dl import flowkey_dl, arange_image, save_png, save_pdf, strip_url
from PIL import ImageTk

dim = {"A4 Landscape": (2338, 1652), "A4 Portrait": (1652, 2338)}


class MainWindow(object):
    def __init__(self, master):
        self._update = None
        self.master = master
        self.master.title(flowkey_dl)
        self.song = Frame(master)
        self.song.grid(row=0, column=0)
        self.layout = Frame(master)
        self.layout.grid(row=1, column=0)
        self.measure = Frame(master)
        self.measure.grid(row=2, column=0)
        self.preview = Frame(master)
        self.preview.grid(row=0, column=1, rowspan=3)
        song = self.song
        self.song_lab = Label(song, text="Song:")
        self.song_lab.grid(row=0, column=0)
        self.title_l = Label(song, text="Title")
        self.title_l.grid(row=1, column=0)
        self.title = Entry(song)
        self.title.grid(row=1, column=1)
        self.artist_l = Label(song, text="Artist/Author/Composer")
        self.artist_l.grid(row=2, column=0)
        self.artist = Entry(song)
        self.artist.grid(row=2, column=1)
        self.url_l = Label(song, text="url")
        self.url_l.grid(row=3, column=0)
        self.url = Entry(song)
        self.url.grid(row=3, column=1)
        self.load_b = Button(song, text="load", command=self.load)
        self.load_b.grid(row=4, column=0)
        self.save_b = Button(song, text="save", command=self.save)
        self.save_b.grid(row=4, column=1)
        layout = self.layout
        self.layout_lab = Label(layout, text="Layout:")
        self.layout_lab.grid(row=0, column=0)
        self.size_lab = Label(layout, text="Page size")
        self.size_lab.grid(row=1, column=0)
        self.size = ttk.Combobox(layout, state="readonly", values=list(dim))
        self.size.bind("<<ComboboxSelected>>",
                       lambda event: self.update_preview(1))
        self.size.set("A4 Portrait")
        self.size.grid(row=1, column=1, columnspan=2)
        self.width, self.height = dim[self.size.get()]
        self.scale_lab = Label(layout, text="sheet scale")
        self.scale_lab.grid(row=2, column=0)
        self.scale = Scale(
            layout, from_=10, to=200,
            orient=HORIZONTAL, command=self.update_preview
        )
        self.scale.set(100)
        self.scale.grid(row=2, column=1, columnspan=2)

        self.font_sz_title_lab = Label(layout, text="Title font size")
        self.font_sz_title_lab.grid(row=3, column=0)
        self.font_sz_title = Scale(
            layout, from_=10, to=100,
            orient=HORIZONTAL, command=self.update_preview
        )
        self.font_sz_title.set(50)
        self.font_sz_title.grid(row=3, column=1)
        self.font_sz_author_lab = Label(layout, text="Author font size")
        self.font_sz_author_lab.grid(row=4, column=0)
        self.font_sz_author = Scale(
            layout, from_=10, to=100,
            orient=HORIZONTAL, command=self.update_preview
        )
        self.font_sz_author.set(30)
        self.font_sz_author.grid(row=4, column=1)
        self.space_lab = Label(layout, text="Spacing")
        self.space_lab.grid(row=5, column=0)
        self.space = Scale(
            layout, from_=10, to=200,
            orient=HORIZONTAL, command=self.update_preview
        )
        self.space.set(50)
        self.space.grid(row=5, column=1, columnspan=2)
        measure = self.measure
        self.measure_lab = Label(measure, text="Measure")
        self.measure_lab.grid(row=0, column=0, columnspan=2)
        self.measure_sel_lab = Label(measure, text="select")
        self.measure_sel_lab.grid(row=1, column=0)
        self.measure_sel = Entry(measure)
        self.measure_sel.grid(row=1, column=1)
        self.measure_pre_lab = Label(measure, text="prevent break")
        self.measure_pre_lab.grid(row=2, column=0)
        self.measure_pre = Entry(measure)
        self.measure_pre.grid(row=2, column=1)
        self.measure_force_lab = Label(measure, text="force break")
        self.measure_force_lab.grid(row=3, column=0)
        self.measure_force = Entry(measure)
        self.measure_force.grid(row=3, column=1)
        self.apply_b = Button(
            measure, text="apply",
            command=lambda x=None: self.update_preview(0)
        )
        self.apply_b.grid(row=4, column=0, columnspan=2)
        preview = self.preview
        self.prev_scale_frame = Frame(preview)
        self.prev_scale_frame.grid(row=0, column=0, columnspan=3)
        self.prev_scale_lab = Label(
            self.prev_scale_frame, text="preview scale")
        self.prev_scale_lab.grid(row=0, column=0)
        self.prev_scale = Scale(
            self.prev_scale_frame,
            from_=10,
            to=100,
            orient=HORIZONTAL,
            command=lambda x=None: self.update_preview(2000),
        )
        self.prev_scale.set(25)
        self.prev_scale.grid(row=0, column=1)
        self.image = None
        self.current_page = 0
        self.canvas = Canvas(
            preview, width=self.prev_width, height=self.prev_height, bg="white"
        )  # 100 dpi
        self.prev_img = [
            ImageTk.PhotoImage(i)
            for i in arange_image(width=self.prev_width,
                                  height=self.prev_height)
        ]
        self.prev_area = self.canvas.create_image(
            0, 0, anchor=NW, image=self.prev_img[self.current_page]
        )
        self.canvas.grid(row=1, column=0, columnspan=3)
        self.pre_b = Button(preview, text="<", command=self.pre_img)
        self.pre_b.grid(row=2, column=0)
        self.preview_lab = Label(
            preview, text=f"Page {self.current_page}/{len(self.prev_img)}"
        )
        self.preview_lab.grid(row=2, column=1)
        self.next_b = Button(preview, text=">", command=self.next_img)
        self.next_b.grid(row=2, column=2)

    def load(self):
        url = self.url.get()
        self.image, title, artist = flowkey_dl(url)
        if artist is not None:
            self.artist.delete(0, END)
            self.artist.insert(0, artist)
        if title is not None:
            self.title.delete(0, END)
            self.title.insert(0, title)
        self.update_preview(1)

    def save(self):
        # save raw
        save_png(self.image, self.url.get(),
                self.artist.get(), self.title.get())

        # save processed
        filename = '_'.join([
            self.artist.get().lower().replace(" ", "_"),
            self.title.get().lower().replace(" ", "_"),
            strip_url(self.url.get())
        ])+'.pdf'
        path = filedialog.asksaveasfilename(
            defaultextension=".pdf", initialfile=filename
        )
        if (
            path is not None
        ):  # asksaveasfile return `None` if dialog closed with "cancel".
            save_pdf(self.processed_images, path)

    def pre_img(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.preview_lab.config(
                text=f"Page {self.current_page}/{len(self.prev_img)}"
            )
            self.canvas.itemconfig(
                self.prev_area, image=self.prev_img[self.current_page]
            )

    def next_img(self):
        if self.current_page + 1 < len(self.prev_img):
            self.current_page += 1
            self.preview_lab.config(
                text=f"Page {self.current_page}/{len(self.prev_img)}"
            )
            self.canvas.itemconfig(
                self.prev_area, image=self.prev_img[self.current_page]
            )

    def update_preview(self, delay=500):
        # delay by half a second, cancle if new call comes in
        if self._update:
            self.master.after_cancel(self._update)
        self._update = self.master.after(delay, self._get_preview)

    def get_images(self):
        return arange_image(
            self.image,
            self.title.get(),
            self.artist.get(),
            self.width,
            self.height,
            scale=self.scale.get() / 100,
            space=int(self.space.get()),
            sel_measures=self.measure_sel.get(),
            break_measures=self.measure_force.get(),
            nobreak_measures=self.measure_pre.get(),
            font_size=self.font_size,
        )

    @property
    def font_size(self):
        return (int(self.font_sz_title.get()), int(self.font_sz_author.get()))

    @property
    def prev_width(self):
        return int(self.width * self.prev_scale.get() / 100)

    @property
    def prev_height(self):
        return int(self.height * self.prev_scale.get() / 100)

    def _get_preview(self):
        self._update = None
        self.width, self.height = dim[self.size.get()]
        self.canvas.config(width=self.prev_width, height=self.prev_height)
        self.processed_images = self.get_images()
        self.prev_img = [
            ImageTk.PhotoImage(i.resize((self.prev_width, self.prev_height)))
            for i in self.processed_images
        ]
        # self.canvas.create_image(0,0,anchor=NW,image=ImageTk.PhotoImage(image))
        self.canvas.itemconfig(
            self.prev_area, image=self.prev_img[self.current_page])


def main():
    root = Tk()
    MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
