pipenv run pyinstaller --clean --icon=icon.ico --add-data "bin_patch.asm;." --distpath . -F --hidden-import="pkg_resources.py2_warn" tool.py
