
_pad = "_"
_punctuation = ';:,.!?¡¿—…"«»“” '
_letters = ['i', 'u', 'o', 'a', 'e', 'b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'm', 'n', 'p', 'r', 'l', 's', 't', 'v', 'y', 'w', 'z', 'bw', 'by', 'cw', 'cy', 'dw', 'fw', 'gw', 'hw', 'kw', 'jw', 'jy', 'ny', 'mw', 'my', 'nw', 'pw', 'py', 'rw', 'ry', 'sw', 'sy', 'tw', 'ty', 'vw', 'vy', 'zw', 'pf', 'ts', 'sh', 'shy', 'mp', 'mb', 'mf', 'mv', 'nc', 'nj', 'nk', 'ng', 'nt', 'nd', 'ns', 'nz', 'nny', 'nyw', 'byw', 'ryw', 'shw', 'tsw', 'pfy', 'mbw', 'mby', 'mfw', 'mpw', 'mpy', 'mvw', 'mvy', 'myw', 'ncw', 'ncy', 'nsh', 'ndw', 'ndy', 'njw', 'njy', 'nkw', 'ngw', 'nsw', 'nsy', 'ntw', 'nty', 'nzw', 'shyw', 'mbyw', 'mvyw', 'nshy', 'nshw', 'nshyw', 'bg', 'pfw', 'pfyw', 'vyw', 'njyw', 'x', 'q']

# Export all symbols:
symbols = [_pad] + list(_punctuation) + _letters

# Special symbol ids
SPACE_ID = symbols.index(" ")
