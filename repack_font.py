import codecs
import json
import os
from hacktools import common, psp


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
            if ord(char) > 0x7e:
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
            else:
                charcode += 0x3020
                if ord(char) >= 0x70:
                    charcode += 2
                if ord(char) >= 0x72:
                    charcode += 13
                newchar = chr(charcode)
            data = json.dumps(glyph)
            f.write("#" + char + "\n" + newchar + "=" + data + "\n")
    psp.repackPGFData(fontin, fontout, fontconftemp, fontbmpin)
    common.copyFile(fontout, fontout2)
    os.remove(fontconftemp)
    common.logMessage("Done!")
