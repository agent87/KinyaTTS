import unicodedata
import re

from kinyatts.tts.text.kinya_number_speller import rw_spell_number
from kinyatts.tts.text.symbols import symbols

# Mappings from symbol to numeric ID and vice versa:
_symbol_to_id = {s: i for i, s in enumerate(symbols)}
_id_to_symbol = {i: s for i, s in enumerate(symbols)}

_VOWELS = {'i', 'u', 'o', 'a', 'e'}
_CONSONANTS = {'b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'm', 'n', 'p', 'r', 'l', 's', 't', 'v', 'y', 'w', 'z', 'bw', 'by', 'cw', 'cy', 'dw', 'fw', 'gw', 'hw', 'kw', 'jw', 'jy', 'ny', 'mw', 'my', 'nw', 'pw', 'py', 'rw', 'ry', 'sw', 'sy', 'tw', 'ty', 'vw', 'vy', 'zw', 'pf', 'ts', 'sh', 'shy', 'mp', 'mb', 'mf', 'mv', 'nc', 'nj', 'nk', 'ng', 'nt', 'nd', 'ns', 'nz', 'nny', 'nyw', 'byw', 'ryw', 'shw', 'tsw', 'pfy', 'mbw', 'mby', 'mfw', 'mpw', 'mpy', 'mvw', 'mvy', 'myw', 'ncw', 'ncy', 'nsh', 'ndw', 'ndy', 'njw', 'njy', 'nkw', 'ngw', 'nsw', 'nsy', 'ntw', 'nty', 'nzw', 'shyw', 'mbyw', 'mvyw', 'nshy', 'nshw', 'nshyw', 'bg', 'pfw', 'pfyw', 'vyw', 'njyw'}


def process_cons(cons, seq):
    if cons in _symbol_to_id:
        seq.append(_symbol_to_id[cons])
    else:
        for c in cons:
            if c in _symbol_to_id:
                seq.append(_symbol_to_id[c])

# mu ba mu mi ri ma ki bi n n ru ka tu bu ku ha ku
Rwanda_Months = {'mutarama', 'gashyantare', 'werurwe', 'mata', 'gicurasi', 'kamena', 'nyakanga', 'kanama', 'nzeli', 'nzeri', 'ukwakira', 'ugushyingo', 'ukuboza'}

def rw_prefix(word:str):
    if (len(word) < 4) or (word.lower() in Rwanda_Months):
        return 'ka'
    if len(word) == 0:
        return 'bi'
    if word[0] in _VOWELS:
        return rw_prefix(word[1:])
    if word[0] == 'n':
        return 'zi'
    if word[0:2] == 'cy':
        return 'ki'
    if word[1] == 'w':
        return word[0:1]+'u'
    if word[1] == 'y':
        return word[0:1]+'i'
    return word[0:2]

def norm_text(string, encoding="utf-8") -> str:
    import re
    string = string.decode(encoding) if isinstance(string, type(b'')) else string
    string = string.replace('`','\'')
    string = string.replace("'", "\'")
    string = string.replace("‘", "\'")
    string = string.replace("’", "\'")
    string = string.replace("‚", "\'")
    string = string.replace("‛", "\'")
    string = string.replace(u"æ", u"ae").replace(u"Æ", u"AE")
    string = string.replace(u"œ", u"oe").replace(u"Œ", u"OE")
    string = unicodedata.normalize('NFKD', string).encode('ascii', 'ignore').decode("ascii").lower()

    string = re.sub('([~!@#$%^&*()_+{}|:"<>?`\-=\[\];\',./])', r' \1 ', string)
    string = re.sub('\s{2,}', ' ', string)

    tokens = string.split()
    final_tokens = []
    for i,tok in enumerate(tokens):
        if tok.isnumeric():
            if i > 0:
                final_tokens.append(rw_spell_number(rw_prefix(tokens[i-1]),int(tok)).strip())
            else:
                final_tokens.append(rw_spell_number('ka', int(tok)).strip())
        else:
            final_tokens.append(tok)
    return ' '.join(final_tokens)

def text_to_sequence(text):
    seq = []
    txt = norm_text(text)
    txt = re.sub(r"\s+", '|', txt).strip()
    start = 0
    end = 0
    while (end < len(txt)):
        if (txt[end] in _VOWELS) or (txt[end] == '|'):
            if (end > start):
                process_cons(txt[start:end], seq)
            if (txt[end] == '|'):
                seq.append(_symbol_to_id[' '])
            else:
                seq.append(_symbol_to_id[txt[end]])
            end += 1
            start = end
        else:
            end += 1
    if (end > start):
        process_cons(txt[start:end], seq)
    return seq

def cleaned_text_to_sequence(text):
  return text_to_sequence(text)

def sequence_to_text(sequence):
    """Converts a sequence of IDs back to a string"""
    result = ""
    for symbol_id in sequence:
        s = _id_to_symbol[symbol_id]
        result += s
    return result

if __name__ == "__main__":
    print(norm_text('55 afite imyaka 19562 gusa'))
