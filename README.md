# Bakemonogatari Translation
This repository is for the tool used to translate the game. If you're looking for the English patch, click [here](http://www.romhacking.net/translations/6638/).  
## Setup
Create a "BakeData" folder and copy the PSP image as "bake.iso" in it.  
Open PPSSPP, go to Settings, Tools, Developer Tools and enable the "Dump decrypted EBOOT.BIN on game boot".  
Run the game, then browse the emulator output folder (on Windows, "Documents\PPSSPP\PSP\SYSTEM\DUMP"), copy the NPJH50605.BIN in the "BakeData" folder and rename it to "BOOT.BIN".  
## Run from binary
Download the latest [release](https://github.com/Illidanz/BakeTranslation/releases) outside the data folder.  
Run `tool extract` to extract everything and `tool repack` to repack after editing.  
Run `tool extract --help` or `tool repack --help` for more info.  
## Run from source
Install [Python 3.8](https://www.python.org/downloads/) and pipenv.  
Download [armips.exe](https://github.com/Kingcom/armips/releases).  
Download UMD-replace.exe.  
Download xdelta.exe.  
Run `pipenv sync`.  
Run the tool with `pipenv run tool.py` or build with `pipenv run pyinstaller tool.spec`.  
## Text Editing
Rename the \*\_output.txt files to \*\_input.txt (str_output.txt to str_input.txt, etc) and add translations for each line after the "=" sign.  
To blank out a line, use a single "!". If just left empty, the line will be left untranslated.  
Comments can be added at the end of lines by using #  
## Image Editing
Rename the out\_\* folders to work\_\* (out_IMG to work_IMG, etc).  
If an image doesn't require repacking, it should be deleted from the work folder.  
