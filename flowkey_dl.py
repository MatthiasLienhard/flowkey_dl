#!/bin/python3
import requests

import imageio

from PIL import Image
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

def find_measure(image):
    #image is a numpy array
    #there are about 20 pixel above and 15 below the lines. 
    # at most 5 pixels can be brighter than 100
    measures=np.where((image>100)[50:-50,:].sum(0)<10) 
    return next(iter(measures))
    #todo: minimal distance: 200 pixel

def arange_image(image=None, title=None, autor=None,width=2480, height=3508, scale=1):
    out=Image.fromarray(255*np.ones((int(height),int(width))))
    if image is None:
        return out
    measures=find_measure(image)
    offset=0
    breaks=list()
    for i,ix in enumerate(measures):
        if ix-offset>width/scale:
            if measures[i-1]>offset:
                breaks.append(measures[i-1])
            else:
                breaks.append(measures[i])
            offset=breaks[-1]
    breaks.append(image.shape[1])
    offset=0
    y=0
    for i,ix in enumerate(breaks):
        print(f'{offset}, {ix}')
        patch=image[:,offset:ix+10]
        dim=patch.shape
        patch=Image.fromarray(patch)
        patch=patch.resize((int(x*scale) for x in reversed(dim)))
        out.paste(patch, (0,y)) 
        y+=patch.height+10
        offset=ix-10    
    return out



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
