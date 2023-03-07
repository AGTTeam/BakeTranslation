import codecs
import os
import game
from hacktools import common, psp


def run(data):
    binin = data + "extract/PSP_GAME/SYSDIR/EBOOT.BIN"
    binout = data + "repack/PSP_GAME/SYSDIR/BOOT.BIN"
    ebinout = data + "repack/PSP_GAME/SYSDIR/EBOOT.BIN"
    binpatch = "bin_patch.asm"

    psp.decryptBIN(binin, binout)
    common.armipsPatch(common.bundledFile(binpatch))
    psp.signBIN(binout, ebinout, 5)
    common.copyFile(binout.replace("repack", "extract"), binout)
