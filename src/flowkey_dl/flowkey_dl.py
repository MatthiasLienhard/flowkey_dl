#!/bin/python3
import requests
import pkg_resources
import imageio
from PIL import Image, ImageDraw, ImageFont
from matplotlib import font_manager
import numpy as np
from PIL.PngImagePlugin import PngImageFile, PngInfo


def flowkey_dl(url):
    # url=os.path.dirname(url)+'/{}.png'
    hashstring = strip_url(url)
    try:
        filename = pkg_resources.resource_filename(
            __name__, f"raw/{hashstring}.png")
        img = PngImageFile(filename)
    except FileNotFoundError:
        pass
    else:
        print(f"found local file {filename}")
        return np.array(img), img.info.get("Title"), img.info.get("Author")
    url = make_url(hashstring)
    # load with
    imgs = list()
    i = 0
    while True:
        # im = imageio.imread(url.format(i))
        r = requests.get(url.format(i))
        if r.content[-6:-1] == b"Error":
            break
        patch = imageio.imread(r.content, format='png', pilmode="RGBA")
        print(f"loaded patch {i} with shape {patch.shape}")
        if len(patch.shape) == 3 and patch.shape[2] == 4:  # rgba
            imgs.append(255 - patch[:, :, 3])
        elif len(patch.shape) == 2:  # bw
            imgs.append(patch)
        else:
            print(f"patch {i} looks strange, " +
                  f"ignoring: {patch} \nshape: {patch.shape}")
        i += 1
    print(f"downloaded {len(imgs)} patches form {url}")
    # print([i.shape for i in imgs])

    return np.hstack(imgs), None, None


def find_measure(image, min_sz=100):
    # image is a numpy array
    # there are about 20 pixel above and 15 below the lines.
    # at most 5 pixels can be brighter than 100

    # 1) find horizontal lines: at most 20% bright pixels
    lines = np.where((image > 100)[:, 50:-50].sum(1) < image.shape[1] * .2)[0]
    # 2) find vertical lines (measures): at most 10 bright pixels
    positions = np.where((image > 100)[lines[0]: lines[-1], :].sum(0) < 10)[0]
    if len(positions):
        measures = [positions[0]]
        for i in positions:
            if i > measures[-1] + min_sz:
                measures.append(i)
        print(f"found {len(measures)-1} measures")
        return measures
    print(
        f"Error: No measures found in image. Darkest point is {image.min()}.")
    print(
        f"Longest Vertical line (>=100) is {(image < 100).sum(0).max()}, should be > {lines[-1]-lines[0]-10}")
    return [0]


def parse_nums(val=None):
    # parse strings like '1,3,6-10,15'
    nums = []
    try:
        if val is not None and val:
            for v in val.split(","):
                if "-" in v:
                    _from, to = v.split("-")
                    nums.extend(list(range(int(_from), int(to) + 1)))
                else:
                    nums.append(int(v))
    except ValueError:
        return []
    return nums


def arange_image(
    image=None,
    title="",
    author="",
    width=2480,
    height=3508,
    scale=1,
    space=50,
    sel_measures=None,
    break_measures=None,
    nobreak_measures=None,
    font_size=(40, 20),
    mar=50,
):
    sel_measures, break_measures, nobreak_measures = [
        parse_nums(val) for val in
        (sel_measures, break_measures, nobreak_measures)
    ]
    out = [Image.fromarray(255 * np.ones((int(height), int(width))))]
    font_type = font_manager.FontProperties(family='serif')
    font_file = font_manager.findfont(font_type)
    fnt = [ImageFont.truetype(font_file, sz) for sz in font_size]
    d = ImageDraw.Draw(out[-1])
    w, h = d.textsize(title, font=fnt[0])
    d.text(((width - w) / 2, mar), title, font=fnt[0], fill=0)
    w2, h2 = d.textsize(author, font=fnt[1])
    d.text((width - mar - w2, mar + h), author, font=fnt[1], fill=0)

    print(f"arage images of size {width}x{height}")
    if image is None:
        return out
    measures = find_measure(image)
    if sel_measures:
        print(f"selecting measures {sel_measures}")
        image = np.hstack(
            [
                image[:, measures[m - 1]: measures[m]]
                for m in sel_measures
                if m < len(measures)
            ]
        )
        # offset=0
        rm = [0]
        # new_measures=list()
        for i, m in enumerate(measures[1:]):
            rm.append(rm[i])
            if i + 1 not in sel_measures:
                # offset+=measures[i]-m
                rm[i + 1] += 1
        nobreak_measures = [v - rm[v]
                            for v in nobreak_measures if v in sel_measures]
        break_measures = [v - rm[v]
                          for v in break_measures if v in sel_measures]
        measures = find_measure(image)

    offset = measures[0]
    breaks = list()
    for i, ix in enumerate(measures):
        if i not in nobreak_measures and (
            ix - offset > (width - 2 * mar) / scale or i in break_measures
        ):
            if measures[i - 1] > offset:
                breaks.append(measures[i - 1])
            else:
                breaks.append(measures[i])
            offset = breaks[-1]
    breaks.append(image.shape[1])
    offset = max(0, measures[0] - 1)
    y = int(mar + h + h2 + space / 2)
    for i, ix in enumerate(breaks):
        print(f"{offset}, {ix}")
        if y + image.shape[0] + mar > height:
            out.append(Image.fromarray(
                255 * np.ones((int(height), int(width)))))
            y = mar
        patch = image[:, offset: ix + 1]
        dim = patch.shape
        patch = Image.fromarray(patch)
        patch = patch.resize((int(x * scale) for x in reversed(dim)))
        out[-1].paste(patch, (mar, y))
        y += patch.height + space
        offset = ix - 1
    return out


def load_image(filename):
    img = PngImageFile(filename)
    return img


def strip_url(url):
    if url.startswith("https://flowkeycdn.com/sheets/"):
        url = url[30:]
        if "/" in url:
            url = url[: url.find("/")]
    return url


def make_url(hashstring, dpi=300):
    if dpi != 300:
        dpi = 150
    return f"https://flowkeycdn.com/sheets/{hashstring}/{dpi}/" + "{}.png"


def save_png(image, url, author, title):
    metadata = PngInfo()
    metadata.add_text("Title", title)
    metadata.add_text("Author", author)
    filename = pkg_resources.resource_filename(
        __name__, f"raw/{strip_url(url)}.png")
    print(f"saving raw image of sheet {author} - {title} to {filename}")
    try:
        Image.fromarray(image).save(filename, pnginfo=metadata)
    except FileNotFoundError:
        print(
            f'Warning: raw image can not be saved, no raw folder found at {filename}')
    except Exception:
        print("Warning: raw image can not be saved, will be downloaded again next time.")
    # load with PngImageFile(filename)


def save_pdf(images, filename):
    images = [i.convert("RGB") for i in images]
    print(f"saving {len(images)} pages to {filename}")
    if len(images) == 1:
        images[0].save(filename)
    else:
        images[0].save(filename, save_all=True, append_images=images[1:])


def main():
    url = "https://flowkeycdn.com/sheets/XXXXX/150/0.png"
    image = flowkey_dl(url)
    measure = find_measure(image)
    r, g, b = [image.copy() for _ in range(3)]
    r[:, measure] = 255
    Image.fromarray(np.dstack([r, g, b])).show()


if __name__ == "__main__":
    main()
