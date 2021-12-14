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
                if "ID14158" in file:
                    # Tweak the first palette for logo file to get a better result
                    with common.Stream(outpath, "rb+") as f:
                        f.seek(amt.textures[1].paldatapos)
                        paldata = f.read(amt.textures[1].paldatasize * 2)
                        f.seek(amt.textures[0].paldatapos)
                        f.write(paldata)
                        amt.textures[0].palette = amt.gim.images[0].palette = amt.textures[1].palette
                psp.writeGIM(outpath, amt.gim, pngfile)
                repacked += 1
    common.logMessage("Done! Repacked", repacked, "files")
