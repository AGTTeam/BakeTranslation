import codecs
import game
from hacktools import common


def run(data, writeid=True):
    infolder = data + "extract_CPK/rom/"
    outfile = data + "str_output.txt"

    common.logMessage("Extracting STR to", outfile, "...")
    with codecs.open(outfile, "w", "utf-8") as out:
        for file in common.showProgress(game.strfiles):
            common.logDebug("Processing", file, "...")
            with common.Stream(infolder + file, "rb") as f:
                out.write("!FILE:" + file + "\n")
                strnum = f.readUInt()
                for i in range(strnum):
                    strlen = f.readUInt()
                    utfstr = game.readString(f, strlen)
                    if writeid:
                        out.write(common.toHex(i) + ": ")
                    out.write(utfstr + "=\n")
    common.logMessage("Done! Extracted", len(game.strfiles), "files")
