import os
import game
from hacktools import common, psp


def run(data):
    infolder = data + "extract_CPK/rom/"
    outfolder = data + "repack_CPK/rom/"
    workfolder = data + "work_IMG/"

    common.logMessage("Repacking IMG from", workfolder, "...")
    files = common.getFiles(infolder, ".amt")
    files.append("loading_icon.amt")
    repacked = 0
    for file in common.showProgress(files):
        pngfile = workfolder + file.replace(".amt", ".png")
        if os.path.isfile(pngfile):
            common.logDebug("Processing", file, "...")
            filepath = infolder + file
            outpath = outfolder + file
            if not os.path.isfile(filepath):
                filepath = filepath.replace("/extract_CPK/rom/", "/extract/PSP_GAME/USRDIR/nowloading/")
                outpath = data + "repack/PSP_GAME/USRDIR/nowloading/" + file
            amt = game.readAMT(filepath)
            if amt is not None:
                common.makeFolders(os.path.dirname(outpath))
                common.copyFile(filepath, outpath)
                psp.writeGIM(outpath, amt.gim, pngfile)
                repacked += 1
    common.logMessage("Done! Repacked", repacked, "files")
