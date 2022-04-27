import codecs
import game
from hacktools import common


class LineStats:
    def __init__(self):
        self.i = 0
        self.storyOrder1 = 0
        self.storyOrder2 = 0
        self.unk2 = 0
        self.alphabeticalOrder1 = 0
        self.alphabeticalOrder2 = 0
        self.alphabeticalOrder3 = 0
        self.alphabeticalOrder4 = 0
        self.index = 0
        self.unk6 = 0
        self.unk7 = 0
        self.unk8 = 0
        self.unk9 = 0
        self.unk10 = 0
        self.unk11 = 0
        self.unk12 = 0
        self.unk13 = 0
        self.unk14 = 0
        self.unk15 = 0
        self.unk16 = 0
        self.type = 0  # 0 = paper, 1 = rock, 2 = scissors
        self.unk18 = 0
        self.unk19 = 0
        self.unk20 = 0
        self.unk21 = 0
        self.unk22 = 0
        self.unk23 = 0
        self.unk24 = 0
        self.unk25 = 0
        self.unk26 = 0
        self.unk27 = 0
        self.unk28 = 0
        self.unk29 = 0
        self.unk30 = 0
        self.unk31 = 0
        self.unk32 = 0
        self.unk33 = 0
        self.unk34 = 0
        self.unk35 = 0
        self.unk36 = 0
        self.unk37 = 0
        self.unk38 = 0
        self.unk39 = 0
        self.unk40 = 0
        self.unk41 = 0
        self.unk42 = 0
        self.unk43 = 0
        self.unk44 = 0
        self.unk45 = 0
        self.unk46 = 0
        self.unk47 = 0
        self.unk48 = 0
        self.unk49 = 0
        self.unk50 = 0
        self.unk51 = 0
        self.unk52 = 0
        self.unk53 = 0
        self.unk54 = 0
        self.unk55 = 0
        self.index2 = 0
        self.index3 = 0
        self.unk58 = 0
        self.unk59 = 0
        self.unk60 = 0
        self.unk61 = 0
        self.unk62 = 0
        self.unk63 = 0
        self.original = ""
        self.translation = ""


def readLines(f):
    lines = []
    num = f.readUInt()
    for i in range(num):
        line = LineStats()
        line.i = i
        line.storyOrder1 = f.readByte()
        line.storyOrder2 = f.readByte()
        line.unk2 = f.readShort()
        line.alphabeticalOrder1 = f.readSByte()
        line.alphabeticalOrder2 = f.readSByte()
        line.alphabeticalOrder3 = f.readSByte()
        line.alphabeticalOrder4 = f.readSByte()
        line.index = f.readShort()
        line.unk6 = f.readShort()
        line.unk7 = f.readShort()
        line.unk8 = f.readShort()
        line.unk9 = f.readShort()
        line.unk10 = f.readShort()
        line.unk11 = f.readShort()
        line.unk12 = f.readShort()
        line.unk13 = f.readShort()
        line.unk14 = f.readShort()
        line.unk15 = f.readShort()
        line.unk16 = f.readShort()
        line.type = f.readShort()
        line.unk18 = f.readShort()
        line.unk19 = f.readShort()
        line.unk20 = f.readShort()
        line.unk21 = f.readShort()
        line.unk22 = f.readShort()
        line.unk23 = f.readShort()
        line.unk24 = f.readShort()
        line.unk25 = f.readShort()
        line.unk26 = f.readShort()
        line.unk27 = f.readShort()
        line.unk28 = f.readShort()
        line.unk29 = f.readShort()
        line.unk30 = f.readShort()
        line.unk31 = f.readShort()
        line.unk32 = f.readShort()
        line.unk33 = f.readShort()
        line.unk34 = f.readShort()
        line.unk35 = f.readShort()
        line.unk36 = f.readShort()
        line.unk37 = f.readShort()
        line.unk38 = f.readShort()
        line.unk39 = f.readShort()
        line.unk40 = f.readShort()
        line.unk41 = f.readShort()
        line.unk42 = f.readShort()
        line.unk43 = f.readShort()
        line.unk44 = f.readShort()
        line.unk45 = f.readShort()
        line.unk46 = f.readShort()
        line.unk47 = f.readShort()
        line.unk48 = f.readShort()
        line.unk49 = f.readShort()
        line.unk50 = f.readShort()
        line.unk51 = f.readShort()
        line.unk52 = f.readShort()
        line.unk53 = f.readShort()
        line.unk54 = f.readShort()
        line.unk55 = f.readShort()
        line.index2 = f.readShort()
        line.index3 = f.readShort()
        line.unk58 = f.readShort()
        line.unk59 = f.readShort()
        line.unk60 = f.readShort()
        line.unk61 = f.readShort()
        line.unk62 = f.readShort()
        line.unk63 = f.readShort()
        # common.logMessage(common.toHex(i), common.varsHex(line))
        lines.append(line)
    return lines


def run(data):
    linesin = data + "extract_CPK/rom/"
    linesout = data + "repack_CPK/rom/"
    strin = data + "str_input.txt"

    common.logMessage("Repacking lines ...")
    repacked = 0
    for i in common.showProgress(range(len(game.linefiles))):
        # Read the original lines from the respective str file
        originals = []
        with common.Stream(linesin + game.wordwrapfiles[i], "rb") as f:
            strnum = f.readUInt()
            for j in range(strnum):
                strlen = f.readUInt()
                originals.append(game.readString(f, strlen))
        # Read the translation
        with codecs.open(strin, "r", "utf-8") as f:
            section = common.getSection(f, game.wordwrapfiles[i])
        # Read the line stats
        file = game.linefiles[i]
        common.copyFile(linesin + file, linesout + file)
        with common.Stream(linesout + file, "r+b") as f:
            lines = readLines(f)
            # This is how the game sorts alphabetically:
            # lines = sorted(lines, key=lambda x: (x.alphabeticalOrder1, x.alphabeticalOrder2, x.alphabeticalOrder3, x.alphabeticalOrder4))
            # Get the original line and translation for each line
            for j in range(len(lines)):
                line = lines[j]
                if line.index > 0 and line.index3 >= 0:
                    line.original = line.translation = originals[line.index - 1]
                    if line.original in section:
                        line.translation = section[line.original].pop(0)
                        if len(section[line.original]) == 0:
                            del section[line.original]
                        line.translation = line.translation.lstrip("|.*‘’“”…※■―-,'\" ?!").replace("</dot1>", "").replace("</dot0>", "")
                    # common.logMessage(common.varsHex(line))
            # Sort the lines
            lines = sorted(lines, key=lambda x: (x.translation))
            # Write the new order
            order1 = order2 = 1
            for j in range(len(lines)):
                line = lines[j]
                if line.index > 0 and line.index3 >= 0 and line.translation != "":
                    common.logDebug("Writing order", order1, order2, common.varsHex(line))
                    f.seek(4 + line.i * 0x7e + 4)
                    f.writeSByte(order1)
                    f.writeSByte(order2)
                    f.writeSByte(1)
                    f.writeSByte(1)
                    order2 += 1
                    if order2 == 100:
                        order1 += 1
                        order2 = 1
        repacked += 1
    common.logMessage("Done! Repacked", repacked, "files")
