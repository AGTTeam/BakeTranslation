# This is a list of AMT files that need their AMA file tweaked in order to fit the translation
# The first element is the corresponding AMA file, and everything else is offset and float to write
files = {
    "ID13756.amt": [
        "ID13755.ama",
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
    ],
}
backwards_pal = [
    "ID14196.amt",
]
