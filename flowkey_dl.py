#!/bin/python3
import requests

import imageio

from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import numpy as np
import os
from PIL.PngImagePlugin import PngImageFile, PngInfo

def flowkey_dl(url):
    url=os.path.dirname(url)+'/{}.png'
    imgs=list()
    i=0
    while True:   
        #im = imageio.imread(url.format(i)) 
        r = requests.get(url.format(i))
        if r.content[-6:-1]==b'Error':
            break
        imgs.append(imageio.get_reader(r.content, '.png'))
        #imgs.append(Image.open(BytesIO(r.content)))
        i+=1
    print(f'downloaded {i} patches form {url}')
    imgs_comb = np.hstack( [next(iter( i )) for i in imgs ] )
    r,g,b,a=np.rollaxis(imgs_comb, axis=-1)
    return 255-a

def find_measure(image, min_sz=100):
    #image is a numpy array
    #there are about 20 pixel above and 15 below the lines. 
    # at most 5 pixels can be brighter than 100
    positions=np.where((image>100)[50:-50,:].sum(0)<10)[0]
    measures=[positions[0]]
    for i in positions:
        if i> measures[-1]+min_sz:
            measures.append(i)
    print(f'found {len(measures)-1} measures')
    return measures

def parse_nums(val=None):
    #parse strings like '1,3,6-10,15'
    nums=[]
    if val is not None and val:
        for v in val.split(','):
            if '-' in v:
                _from, to= v.split('-')
                nums.extend(list(range(int(_from), int(to)+1)))
            else:
                nums.append(int(v))
    return nums


def arange_image(image=None, title='', author='',width=2480, height=3508, scale=1,space=50, sel_measures=None,break_measures=None, nobreak_measures=None,font_size=(40,20) ):
    mar=20
    sel_measures,break_measures, nobreak_measures=[parse_nums(val) for val in (sel_measures,break_measures, nobreak_measures)]
    out=[Image.fromarray(255*np.ones((int(height),int(width))))]
    fnt = [ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', sz) for sz in font_size]
    d = ImageDraw.Draw(out[-1])
    w, h = d.textsize(title, font=fnt[0])
    d.text(((width-w)/2,mar),title, font=fnt[0], fill=0)
    w2, h2= d.textsize(author, font=fnt[1])
    d.text((width-mar-w2,mar+h), author, font=fnt[1], fill=0)

    print(f'arage images of size {width}x{height}')
    if image is None:
        return out
    measures=find_measure(image)
    if sel_measures:
        print(f'selecting measures {sel_measures}')
        image=np.hstack([image[:,measures[m-1]:measures[m]] for m in sel_measures])
        #offset=0
        rm=[0]
        #new_measures=list()
        for i,m in enumerate(measures[1:]):
            rm.append(rm[i])
            if i+1 not in sel_measures:
                #offset+=measures[i]-m
                rm[i+1]+=1
        nobreak_measures=[v-rm[v] for v in nobreak_measures if v in sel_measures]
        break_measures=[v-rm[v] for v in break_measures if v in sel_measures]
        measures=find_measure(image)

    
    offset=measures[0]
    breaks=list()
    for i,ix in enumerate(measures):
        if i not in nobreak_measures and (ix-offset>(width-2*mar)/scale or i in break_measures):
            if measures[i-1]>offset:
                breaks.append(measures[i-1])
            else:
                breaks.append(measures[i])
            offset=breaks[-1]
    breaks.append(image.shape[1])
    offset=measures[0]
    y=int(mar+h+h2+space/2)
    for i,ix in enumerate(breaks):
        print(f'{offset}, {ix}')
        if y>height-mar:
            out.append(Image.fromarray(255*np.ones((int(height),int(width)))))
            y=mar
        patch=image[:,offset:ix+10]
        dim=patch.shape
        patch=Image.fromarray(patch)
        patch=patch.resize((int(x*scale) for x in reversed(dim)))
        out[-1].paste(patch, (mar,y)) 
        y+=patch.height+space

        offset=ix-10    
    return out

def load_image(filename):
    img=PngImageFile(filename)
    return(img)


def save_image(image, filename, author, title):
    metadata = PngInfo()
    metadata.add_text("Title", title)
    metadata.add_text("Author", author)
    Image.fromarray(image).save(filename, pnginfo=metadata) 
    #load with PngImageFile(filename)

if __name__ == "__main__":
    url = 'https://flowkeycdn.com/sheets/XXXXX/150/0.png'
    image=flowkey_dl(url)
    measure=find_measure(image)
    r,g,b=[image.copy() for _ in range(3)]
    r[:,measure]=255
    Image.fromarray( np.dstack([r,g,b])).show()
