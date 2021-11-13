import math
from hacktools import common, psp

strfiles = [
    "ID08373.bin", "ID08374.bin", "ID08375.bin", "ID08376.bin",
    "ID14266.bin", "ID14267.bin", "ID14268.bin", "ID14269.bin",
    "ID14270.bin", "ID14271.bin", "ID14272.bin", "ID14273.bin", "ID14274.bin", "ID14275.bin", "ID14276.bin", "ID14277.bin", "ID14278.bin",
]


def readString(f, length):
    ret = ""
    start = f.tell()
    while f.tell() < start + length:
        charcode = f.readUShort()
        if charcode == 0xa:
            ret += "|"
        elif charcode != 0:
            ret += chr(charcode)
    return ret.replace("</icon=", "</icon")


def writeString(f, s):
    s = s.replace("</icon", "</icon=")
    lenoffset = f.tell()
    f.writeUInt(0)
    for c in s:
        if c == "|":
            f.writeUShort(0xa)
        else:
            f.writeUShort(ord(c))
    f.writeUShort(0)
    # Align to 4 bytes
    if f.tell() % 4 > 0:
        f.writeZero(4 - (f.tell() % 4))
    f.writeUIntAt(lenoffset, f.tell() - lenoffset - 4)


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
        image.blockedwidth = math.ceil(image.width / image.tilewidth) * image.tilewidth
        image.blockedheight = math.ceil(image.height / image.tileheight) * image.tileheight
        amt.gim.images.append(image)
    return amt
