# flowkey_dl

A python app to download sheet music from flowkey and save it as pdf. 

## installation
```
git clone https://github.com/MatthiasLienhard/flowkey_dl.git
cd flowkey_dl
pip install .
```

## usage:
In a terminal, run
```
flowkey-dl

```
Go to flowkey.com, select a song or lesson and right click on the sheet track at the bottom of the page. Select "Copy image adress" and paste this url (e.g. https://flowkeycdn.com/sheets/XXXX/150/0.png) into the url filed of the app. Click on "load" and the sheet is downloaded and aranged. If you enter title and author, it gets added to the sheet. Optionally adjust layout, scale and font size and select measures (e.g.  1,3,5-10 would select only measures 1, 3 and 5 to 10). Click save to save the sheet as pdf. 
