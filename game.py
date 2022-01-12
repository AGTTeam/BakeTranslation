import math
from hacktools import common, psp

strfiles = [
    "ID08373.bin", "ID08374.bin", "ID08375.bin", "ID08376.bin",
    "ID14266.bin", "ID14267.bin", "ID14268.bin", "ID14269.bin",
    "ID14270.bin", "ID14271.bin", "ID14272.bin", "ID14273.bin", "ID14274.bin", "ID14275.bin", "ID14276.bin", "ID14277.bin", "ID14278.bin",
]

# This is a list of AMT files that need their AMA file tweaked in order to fit the translation
# The first element is the corresponding AMA file, and everything else is offset and float to write
files = {
    "ID13756.amt": [
        "ID13755.ama",
        # Increase texture height from 48 to 64
        (0x25c, 64),
        (0x39c, 64),
        (0x46c, 64),
        (0x53c, 64),
        (0x67c, 64),
        (0x144, -32),
        (0x14c, 32),
        (0x284, -32),
        (0x28c, 32),
        (0x3c4, -32),
        (0x3cc, 32),
        (0x494, -32),
        (0x49c, 32),
        (0x564, -32),
        (0x56c, 32),
        # Move the one at the bottom of the screen up 8 pixels
        (0x1d4, 205),
        (0x1f4, 205),
        # Move the centered one down 10 pixels
        (0x404, 140),
    ],
    "ID13936.amt": [
        "ID13935.ama",
        # Change the 4th texture of Oshino's name to not repeat
        (0x1160, 96),
        (0x1168, 128),
    ],
    "ID13984.amt": [
        "ID13983.ama",
        # Move the text close together
        (0x9c0, 230),
        (0xb10, 246),
    ],
    "ID13734.amt": [
        "ID13733.ama",
        # Move the first half to the right, there are 2 positions since it's animated
        (0xb60, 353),  # 353
        (0xb80, 323),  # 323
        (0xe10, 107),  # 107
        (0xe30, 70),   # 70
        # Move the second half to the left
        (0xca0, 415),  # 415
        (0xcc0, 410),  # 410
        (0xf50, 183),  # 183
        (0xf70, 133),  # 133
    ],
}
backwards_pal = [
    "ID14154.amt",
    "ID14196.amt",
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
