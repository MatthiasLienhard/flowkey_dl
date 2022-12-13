# flowkey_dl

A python app to download sheet music from flowkey and save it as pdf.

## installation

This is a python3 app, that can be installed with pip:

```
python3 -m pip install flowkey_dl
```

To get the latest dev version from git, clone the repository and install from the folder. 
```
git clone https://github.com/MatthiasLienhard/flowkey_dl.git
cd flowkey_dl
python3 -m pip install .
```

The gui of the app depends on tkinter which should be included with all standard Python distributions. If you get import errors, try installing it manually, e.g. in linux with

```
sudo apt-get install python3-tk
```

## usage:

### GUI:

In a terminal, run

```
flowkey-dl

```

~~Go to flowkey.com, select a song or lesson and right click on the sheet track at the bottom of the page.~~
Flowkey made it harder to get the url of the underlying images, simply right click does not work anymore. It should still work when looking in the browsers cache. With google-chrome browser, you find it by clicking on the three dots in the top right -> more tools -> developer tools, then on the "sources" tab. Here you should find flowkeycdn.com with a folder /sheets, with all the songs from the last session. Click right on the first image (0.png) and then 'copy link location'. There is probably similar ways in other browsers.

Paste this url (e.g. https://flowkeycdn.com/sheets/XXXX/300/0.png) into the url filed of the app. Click on "load" and the sheet is downloaded and aranged. If you enter title and author, it gets added to the sheet. Optionally adjust layout, scale and font size and select measures (e.g. 1,3,5-10 would select only measures 1, 3 and 5 to 10). Click save to save the sheet as pdf.

If the font size does not change, you probably do not have the fonts installed. Try installing either FreeMono or arial as ttf.

### CLI:

To start the command line interface run

```bash
flowkey-dl-cli <URL> [<PDF-Output-Path>] [-t <title>] [-a <artist>]
```

This will download the sheet music for the provided flowkey url and export it in pdf format.

The base url refers to the url from flowkey as described above (e.g. https://flowkeycdn.com/sheets/XXXX/<...>) and is required.
