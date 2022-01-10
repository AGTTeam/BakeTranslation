import codecs
import os
import game
from hacktools import common


def extract(data, writeid=False):
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


def repack(data):
    infolder = data + "extract_CPK/rom/"
    outfolder = data + "repack_CPK/rom/"
    # fontconfig = "data/fontconfig.txt"
    infile = data + "str_input.txt"
    chartot = transtot = 0

    if not os.path.isfile(infile):
        common.logError("Input file", infile, "not found")
        return

    # glyphs = game.readFontGlyphs(fontconfig)

    common.logMessage("Repacking STR from", infile, "...")
    common.makeFolders(outfolder)
    with codecs.open(infile, "r", "utf-8") as input:
        for file in common.showProgress(game.strfiles):
            section = common.getSection(input, file)
            common.logDebug(section)
            chartot, transtot = common.getSectionPercentage(section, chartot, transtot)
            # Repack the file
            common.logDebug("Processing", file, "...")
            size = os.path.getsize(infolder + file)
            with common.Stream(infolder + file, "rb") as fin:
                common.makeFolders(os.path.dirname(outfolder + file))
                with common.Stream(outfolder + file, "wb") as f:
                    strnum = fin.readUInt()
                    f.writeUInt(strnum)
                    for i in range(strnum):
                        strlen = fin.readUInt()
                        check = game.readString(fin, strlen)
                        newutf = ""
                        if check in section:
                            newutf = section[check].pop(0)
                            # common.logMessage(newutf)
                            if len(section[check]) == 0:
                                del section[check]
                        if newutf != "":
                            # newutf = common.wordwrap(newutf, glyphs, game.wordwrap)
                            game.writeString(f, newutf)
                        else:
                            game.writeString(f, check)
    common.logMessage("Done! Translation is at {0:.2f}%".format((100 * transtot) / chartot))
