import codecs
import json
import os
from hacktools import common, psp


specialchars = {
    0x2015: 0x30af,  # ―
    0x2018: 0x30b0,  # ‘
    0x2019: 0x30b1,  # ’
    0x201c: 0x30b2,  # “
    0x201d: 0x30b3,  # ”
    0x2026: 0x30ae,  # …
}


def run(data):
    fontin = data + "extract/PSP_GAME/USRDIR/rom/font/ESC_HGPMB.pgf"
    fontout = data + "repack/PSP_GAME/USRDIR/rom/font/ESC_HGPMB.pgf"
    fontout2 = data + "repack_CPK/rom/ID08360.bin"
    fontbmpin = data + "work_FONT/"
    fontconfin = data + "fontconfig_input.txt"
    fontconftemp = data + "fontconfig_temp_output.txt"

    common.logMessage("Repacking font from", fontconfin, "...")
    with codecs.open(fontconfin, "r", "utf-8") as f:
        section = common.getSection(f, "", "##")
    common.copyFile(fontconfin, fontconftemp)
    with codecs.open(fontconftemp, "a", "utf-8") as f:
        for char in section:
            glyph = json.loads(section[char][0])
            char = char.replace("<3D>", "=")
            if ord(char) > 0x7e and ord(char) not in specialchars:
                continue
            glyph["width"], glyph["height"] = glyph["height"], glyph["width"]
            glyph["left"], glyph["top"] = glyph["top"], glyph["left"]
            glyph["dimension"]["x"], glyph["dimension"]["y"] = glyph["dimension"]["y"], glyph["dimension"]["x"]
            glyph["bearingx"]["x"], glyph["bearingx"]["y"] = glyph["bearingx"]["y"], glyph["bearingx"]["x"]
            glyph["bearingy"]["x"], glyph["bearingy"]["y"] = glyph["bearingy"]["y"], glyph["bearingy"]["x"]
            glyph["advance"]["x"], glyph["advance"]["y"] = glyph["advance"]["y"], glyph["advance"]["x"]
            glyph["bearingx"]["y"] = -10
            charcode = ord(char)
            if charcode == 0x20:
                newchar = chr(0x3005)
            elif charcode in specialchars:
                newchar = chr(specialchars[charcode])
            else:
                charcode += 0x3020
                if ord(char) >= 0x70:
                    charcode += 2
                if ord(char) >= 0x72:
                    charcode += 13
                newchar = chr(charcode)
            if "vertwidth" in glyph:
                glyph["width"] = glyph["vertwidth"]
            fontdata = json.dumps(glyph)
            f.write("#" + char + "\n" + newchar + "=" + fontdata + "\n")
    psp.repackPGFData(fontin, fontout, fontconftemp, fontbmpin)
    common.makeFolders(data + "repack_CPK/rom")
    common.copyFile(fontout, fontout2)
    os.remove(fontconftemp)
    common.logMessage("Done!")
