import os
from hacktools import common, psp


def run(data):
    moviesin = data + "work_MPS/"
    cpkout = data + "extract_CPK/"

    common.logMessage("Repacking movies ...")
    for file in common.getFiles(moviesin):
        pmffile = file.replace(".MPS", ".pmf")
        # Get the original length for the PMF file
        pmffolder = cpkout + "exrom/"
        if not os.path.isfile(pmffolder + pmffile):
            pmffolder = pmffolder.replace("exrom", "rom")
        with common.Stream(pmffolder + pmffile, "rb", False) as f:
            f.seek(0x5c)
            totlength = f.readUInt()
        # Write the new header
        psp.mpstopmf(moviesin + file, pmffolder.replace("extract_", "repack_") + pmffile, totlength)
    common.logMessage("Done!")
