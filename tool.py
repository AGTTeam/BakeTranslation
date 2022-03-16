import os
import click
import game
from hacktools import common, cpk, psp

version = "0.9.0"
data = "BakeData/"
isofile = data + "bake.iso"
isopatch = data + "bake_patched.iso"
patchfile = data + "patch.xdelta"

infolder = data + "extract/"
outfolder = data + "repack/"
replacefolder = data + "replace/"
cpkin = infolder + "PSP_GAME/USRDIR/rom/"
cpkout = data + "extract_CPK/"
replacecpkfolder = data + "replace_CPK/"

fontin = data + "extract/PSP_GAME/USRDIR/rom/font/ESC_HGPMB.pgf"
fontbmpout = data + "out_FONT/"
fontconfout = data + "fontconfig_output.txt"

@common.cli.command()
@click.option("--iso", is_flag=True, default=False)
@click.option("--cpk", "cpkparam", is_flag=True, default=False)
@click.option("--str", "strparam", is_flag=True, default=False)
@click.option("--img", is_flag=True, default=False)
@click.option("--font", is_flag=True, default=False)
def extract(iso, cpkparam, strparam, img, font):
    all = not iso and not cpkparam and not strparam and not img and not font
    if all or iso:
        psp.extractIso(isofile, infolder, outfolder)
    if all or cpkparam:
        common.makeFolder(cpkout)
        common.logMessage("Extracting CPK ...")
        cpk.extract(cpkin + "rom.cpk", cpkout + "rom/", guessRomExtension)
        common.logMessage("Done!")
        common.logMessage("Extracting Movies CPK ...")
        cpk.extract(cpkin + "exrom.cpk", cpkout + "exrom/", guessExromExtension)
        common.logMessage("Done!")
    if all or strparam:
        import format_str
        format_str.extract(data)
    if all or img:
        import format_img
        format_img.extract(data)
    if all or font:
        common.logMessage("Extracting font to", fontconfout, "...")
        common.makeFolder(fontbmpout)
        psp.extractPGFData(fontin, fontconfout, fontbmpout)
        common.logMessage("Done!")


@common.cli.command()
@click.option("--no-iso", is_flag=True, default=False)
@click.option("--cpk", "cpkparam", is_flag=True, default=False)
@click.option("--str", "strparam", is_flag=True, default=False)
@click.option("--mov", is_flag=True, default=False)
@click.option("--img", is_flag=True, default=False)
@click.option("--bin", is_flag=True, default=False)
@click.option("--font", is_flag=True, default=False)
def repack(no_iso, cpkparam, strparam, mov, img, bin, font):
    all = not cpkparam and not strparam and not mov and not img and not bin and not font
    if all or font:
        import repack_font
        repack_font.run(data)
    if all or strparam:
        import format_str
        format_str.repack(data)
    if all or bin:
        import repack_bin
        repack_bin.run(data)
    if all or mov:
        import repack_mov
        repack_mov.run(data)
    if all or img:
        import format_img
        format_img.repack(data)
    if all or cpkparam or strparam or mov or img:
        common.logMessage("Repacking CPK ...")
        common.mergeFolder(replacecpkfolder, data + "repack_CPK/rom/")
        cpk.repack(cpkin + "rom.cpk", cpkin.replace("extract", "repack") + "rom.cpk", cpkout + "rom/", data + "repack_CPK/rom/")
        common.logMessage("Done!")
    if all or cpkparam or mov:
        common.logMessage("Repacking Movies CPK ...")
        cpk.repack(cpkin + "exrom.cpk", cpkin.replace("extract", "repack") + "exrom.cpk", cpkout + "exrom/", data + "repack_CPK/exrom/")
        common.logMessage("Done!")
    if os.path.isdir(replacefolder):
        common.mergeFolder(replacefolder, outfolder)

    if not no_iso:
        psp.repackUMD(isofile, isopatch, outfolder, patchfile)


@common.cli.command()
def names():
    tot = 0
    totfiles = 0
    for file in common.getFiles(data + "extract_CPK/rom/", ".bin"):
        with common.Stream(data + "extract_CPK/rom/" + file, "rb") as f:
            try:
                strnum = f.readUInt()
                firstlen = f.readUInt()
                firststr = f.readNullString()
            except:
                firststr = ""
            if strnum > 0 and strnum < 0x1000 and firstlen > 0 and firstlen < 0x100 and len(firststr) > 5:
                if common.isAscii(firststr):
                    common.logMessage("Found names file", file, strnum, firstlen, firststr)
                    tot += strnum
                    totfiles += 1
                else:
                    common.logMessage("Found str file?", file, strnum, firstlen, firststr)
    common.logMessage(totfiles, tot)


@common.cli.command()
@click.argument("text")
def translate(text):
    ret = ""
    for c in text:
        charcode = ord(c)
        charhex = common.toHex(charcode).zfill(4)
        ret += charhex[2:4] + charhex[0:2]
    common.logMessage(ret)
    searchbytes = bytes.fromhex(ret)
    for file in common.getFiles(cpkout):
        with common.Stream(cpkout + file, "rb") as f:
            alldata = f.read()
            pos = alldata.find(searchbytes)
            if pos >= 0:
                common.logMessage("Found string at", common.toHex(pos), "in file", file)


@common.cli.command()
@click.argument("text")
def translatevert(text):
    ret = ""
    for c in text:
        charcode = ord(c)
        if charcode == 0x20:
            ret += chr(0x3005)
        else:
            charcode += 0x3020
            if ord(c) >= 0x70:
                charcode += 2
            if ord(c) >= 0x72:
                charcode += 13
            ret += chr(charcode)
    common.logMessage(ret)


@common.cli.command()
@click.argument("file")
def ama(file):
    import format_img
    format_img.readAMA(cpkout + "rom/" + file)


@common.cli.command()
@click.argument("text")
def length(text):
    glyphs = game.readFontGlyphs(data + "fontconfig_input.txt")
    lookup = dict((c, glyphs[c].length if c in glyphs else 16) for c in set(text))
    ret = 0
    for c in text:
        ret += lookup[c]
    common.logMessage(ret)


@common.cli.command()
def copymovies():
    for filename in common.showProgress(common.getFiles(data + "movies/original_pmf/")):
        filename = filename.replace(".pmf", "")
        umdpath = os.path.expanduser("~/Documents/UmdStreamComposer/MuxWork/" + filename + "/00001/00001.MPS").replace("\\", "/")
        if os.path.isfile(umdpath):
            common.copyFile(umdpath, data + "work_MPS/" + filename + ".MPS")


def guessRomExtension(data, entry, filename):
    import struct
    magicint = struct.unpack('<I', data[:4])[0]
    magicshort = struct.unpack('<H', data[:2])[0]
    magicstr = data[:4].decode('ascii', 'ignore')
    if entry.id == 8067 or entry.id == 8068 or entry.id == 8069:
        return filename + ".png"
    if magicstr == "#AMA":
        return filename + ".ama"
    if magicstr == "#AMB":
        return filename + ".amb"
    if magicstr == "#AMC":
        return filename + ".amc"
    if magicstr == "#AME":
        return filename + ".ame"
    if magicstr == "#AMM":
        return filename + ".amm"
    if magicstr == "#AMO":
        return filename + ".amo"
    if magicstr == "#AMT":
        return filename + ".amt"
    if magicstr == "#BSK":
        return filename + ".bsk"
    if magicstr == "PSMF":
        return filename + ".pmf"
    if magicstr == "PPHD":
        return filename + ".phd"
    if magicshort == 0x80 and magicint != 0x80:
        return filename + ".adx"
    # common.logDebug("Unknown file guess:", filename, common.toHex(magicint), common.toHex(magicshort), magicstr)
    return filename + ".bin"


def guessExromExtension(data, entry, filename):
    magicstr = data[:4].decode('ascii', 'ignore')
    if magicstr == "PSMF":
        return filename + ".pmf"
    return filename + ".adx"


if __name__ == "__main__":
    click.echo("BakeTranslation version " + version)
    if not os.path.isdir(data):
        common.logError(data, "folder not found.")
        quit()
    common.runCLI(common.cli)
