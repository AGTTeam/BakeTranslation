import math
import os
import game
from hacktools import common, psp


class AMTFile:
    def __init__(self):
        self.texnum = 0
        self.offsetpos = 0
        self.texoffsets = []
        self.textures = []
        self.gim = None


class AMTTexture:
    def __init__(self):
        self.id = 0
        self.unk1 = 0
        self.unk2 = 0
        self.unk3 = 0
        self.unk4 = 0
        self.format = 0
        self.unk6 = 0
        self.unk7 = 0
        self.unk8 = 0
        self.unk9 = 0
        self.unk10 = 0
        self.width = 0
        self.height = 0
        self.texdatapos = 0
        self.texdatasize = 0
        self.unk15 = 0
        self.unk16 = 0
        self.paldatapos = 0
        self.paldatasize = 0
        self.unk19 = 0
        self.colors = []
        self.palette = []


def readAMT(file):
    with common.Stream(file, "rb") as f:
        magic = f.readString(4)
        if magic != "#AMT":
            common.logError("Wrong magic", magic, "for file", file)
            return None
        amt = AMTFile()
        f.seek(0x10)
        amt.texnum = f.readUInt()
        amt.offsetpos = f.readUInt()
        common.logDebug("File", vars(amt))
        f.seek(amt.offsetpos)
        for i in range(amt.texnum):
            amt.texoffsets.append(f.readUInt())
        for i in range(amt.texnum):
            f.seek(amt.texoffsets[i])
            texture = AMTTexture()
            texture.id = f.readUInt()
            texture.unk1 = f.readByte()
            texture.unk2 = f.readByte()
            texture.unk3 = f.readByte()
            texture.unk4 = f.readByte()
            texture.format = f.readByte()
            texture.unk6 = f.readByte()
            texture.unk7 = f.readByte()
            texture.unk8 = f.readByte()
            texture.unk9 = f.readUShort()
            texture.unk10 = f.readUShort()
            texture.width = f.readUShort()
            texture.height = f.readUShort()
            texture.texdatapos = f.readUInt()
            texture.texdatasize = f.readUInt()
            texture.unk15 = f.readUInt()
            texture.unk16 = f.readUInt()
            texture.paldatapos = f.readUInt()
            texture.paldatasize = f.readUInt()
            texture.unk19 = f.readUInt()
            common.logDebug("Texture", i, vars(texture))
            f.seek(texture.texdatapos)
            for i in range(texture.height):
                for j in range(texture.width):
                    index = 0
                    if texture.format == 0x04:
                        index = f.readHalf()
                    elif texture.format == 0x05:
                        index = f.readByte()
                    else:
                        index = psp.readColor(f, 0x03)
                    texture.colors.append(index)
            f.seek(texture.paldatapos)
            while f.tell() < texture.paldatapos + texture.paldatasize:
                palcolor = psp.readColor(f, 0x03)
                palalpha = palcolor[3]
                # if texture.format == 0x05:
                #    palalpha = 255
                texture.palette.append((palcolor[0], palcolor[1], palcolor[2], palalpha))
            amt.textures.append(texture)
    # Convert this to a GIM-like file
    amt.gim = psp.GIM()
    for texture in amt.textures:
        image = psp.GIMImage()
        image.width = texture.width
        image.height = texture.height
        image.colors = texture.colors
        image.palette = texture.palette
        image.tiled = 0x01
        if texture.format == 0x03:
            image.bpp = 32
        elif texture.format == 0x04:
            image.bpp = 4
        elif texture.format == 0x05:
            image.bpp = 8
        image.tilewidth = 0x80 // image.bpp
        image.tileheight = 8
        image.imgoff = -32
        image.imgframeoff = texture.texdatapos
        image.format = 0x03 if texture.format != 0x04 and texture.format != 0x05 else texture.format
        image.blockedwidth = math.ceil(image.width / image.tilewidth) * image.tilewidth
        image.blockedheight = math.ceil(image.height / image.tileheight) * image.tileheight
        amt.gim.images.append(image)
    return amt


def extract(data):
    infolder = data + "extract_CPK/rom/"
    outfolder = data + "out_IMG/"

    common.logMessage("Extracting IMG to", outfolder, "...")
    common.makeFolder(outfolder)
    files = common.getFiles(infolder, ".amt")
    files.append("loading_icon.amt")
    for file in common.showProgress(files):
        common.logDebug("Processing", file, "...")
        filepath = infolder + file
        if not os.path.isfile(filepath):
            filepath = filepath.replace("/extract_CPK/rom/", "/extract/PSP_GAME/USRDIR/nowloading/")
        amt = readAMT(filepath)
        if amt is not None:
            outfile = outfolder + file.replace(".amt", ".png")
            psp.drawGIM(outfile, amt.gim)
    common.logMessage("Done! Extracted", len(files), "files")


def repack(data):
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
            amt = readAMT(filepath)
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
                psp.writeGIM(outpath, amt.gim, pngfile, file in game.backwards_pal)
                repacked += 1
                if file in game.files:
                    amadata = game.files[file]
                    amain = filepath.replace(file, amadata[0])
                    amaout = amain.replace("extract_CPK", "repack_CPK")
                    common.copyFile(amain, amaout)
                    with common.Stream(amaout, "rb+") as f:
                        for i in range(1, len(amadata)):
                            f.seek(amadata[i][0])
                            f.writeFloat(amadata[i][1])
    common.logMessage("Done! Repacked", repacked, "files")
