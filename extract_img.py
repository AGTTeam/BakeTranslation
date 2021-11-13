import game
from hacktools import common, psp


def run(data):
    infolder = data + "extract_CPK/rom/"
    outfolder = data + "out_IMG/"

    common.logMessage("Extracting IMG to", outfolder, "...")
    common.makeFolder(outfolder)
    files = common.getFiles(infolder, ".amt")
    for file in common.showProgress(files):
        common.logDebug("Processing", file, "...")
        amt = game.readAMT(infolder + file)
        if amt is not None:
            outfile = outfolder + file.replace(".amt", ".png")
            psp.drawGIM(outfile, amt.gim)
    common.logMessage("Done! Extracted", len(files), "files")
