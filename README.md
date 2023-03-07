# Bakemonogatari Translation
## Setup
Create a "BakeData" folder and copy the PSP image as "bake.iso" in it.  
## Run from binary
Download the latest [release](https://github.com/Illidanz/BakeTranslation/releases) outside the data folder.  
Run `tool extract` to extract everything and `tool repack` to repack after editing.  
Run `tool extract --help` or `tool repack --help` for more info.  
## Run from source
Install [Python 3](https://www.python.org/downloads/) and pipenv.  
Run `pipenv sync`.  
Run the tool with `pipenv run tool.py` or build with `pipenv run pyinstaller tool.spec`.  
## Text Editing
Rename the \*\_output.txt files to \*\_input.txt (str_output.txt to str_input.txt, etc) and add translations for each line after the "=" sign.  
To blank out a line, use a single "!". If just left empty, the line will be left untranslated.  
Comments can be added at the end of lines by using #  
## Image Editing
Rename the out\_\* folders to work\_\* (out_IMG to work_IMG, etc).  
If an image doesn't require repacking, it should be deleted from the work folder.  
