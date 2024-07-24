from typing import Union

vowels = {'i', 'u', 'o', 'a', 'e'}

def hundreds(n:int) -> Union[str,None]:
    D = {1:'ijana',
         2:'magana abiri',
         3:'magana atatu',
         4:'magana ane',
         5:'magana atanu',
         6:'magana atandatu',
         7:'magana arindwi',
         8:'magana inani',
         9:'magana cyenda'}
    if n in D:
        return D[n]
    else:
        return None

def tens(n:int) -> Union[str,None]:
    D = {1:'cumi',
         2:'makumyabiri',
         3:'mirongo itatu',
         4:'mirongo ine',
         5:'mirongo itanu',
         6:'mirongo itandatu',
         7:'mirongo irindwi',
         8:'mirongo inani',
         9:'mirongo cyenda'}
    if n in D:
        return D[n]
    else:
        return None

def units(prefix:str,n:int) -> Union[str,None]:
    D_norm = {1:'mwe',
         2:'biri',
         3:'tatu',
         4:'ne',
         5:'tanu',
         6:'tandatu',
         7:'rindwi',
         8:'umunani',
         9:'icyenda'}

    D_zi = {1:'imwe',
         2:'ebyiri',
         3:'eshatu',
         4:'enye',
         5:'eshanu',
         6:'esheshatu',
         7:'zirindwi',
         8:'umunani',
         9:'icyenda'}

    if (n == 8) or (n == 9):
        return D_norm[n]

    if prefix == 'zi':
        if n in D_zi:
            return D_zi[n]
        else:
            raise Exception("Invalid number for zi")
    pair_classes = {'ba':'u',
                    'i':'u',
                    'a':'ri',
                    'bi':'ki',
                    'tu':'ka'}
    single_prefixes = {'ru','ku'}
    cross_prefixes = {'ha','ka'}
    # if (prefix in single_prefixes) and (n != 1):
    #     raise Exception("Invalid prefix number combination")
    if n in D_norm:
        suffix = D_norm[n]
        if prefix in pair_classes:
            if n == 1:
                prefix = pair_classes[prefix]
        if suffix[0:1] == 't':
            if prefix == 'ka':
                prefix = 'ga'
            if prefix == 'ku':
                prefix = 'gu'
            if prefix == 'tu':
                prefix = 'du'
        return prefix+suffix
    else:
        raise Exception("Invalid units number")

def hundreds_tens_units(prefix, n:int)->str:
    if n == 10:
        return 'icumi'
    h = n//100
    t = (n%100)//10
    u = (n%10)

    str = ''
    if u > 0:
        str = units(prefix,u)
        if (t>0) or (h>0):
            str = (' n\'' if (str[0:1] in vowels) else ' na ') + str
    if t > 0:
        t_str = tens(t)
        if (h>0):
            t_str = ' na '+ t_str
        str = t_str + str
    if (h > 0):
        str = hundreds(h) + str
    return str

def thousands(n:int)->Union[str,None]:
    if n > 0:
        return 'ibihumbi '+hundreds_tens_units('bi', n)
    else:
        return None
def millions(n:int)->Union[str,None]:
    if n > 0:
        return 'miliyoni '+hundreds_tens_units('zi', n)
    else:
        return None
def billions(n:int)->Union[str,None]:
    if n > 0:
        return 'miliyari '+hundreds_tens_units('zi', n)
    else:
        return None

def trillions(n:int)->Union[str,None]:
    if n > 0:
        return 'miliyaridi '+hundreds_tens_units('zi', n)
    else:
        return None

def rw_spell_number(prefix, n:int)->Union[str,None]:
    tr = (n//1000_000_000_000)%1000
    bi = (n%1000_000_000_000)//1000_000_000
    mi = (n%1000_000_000)//1000_000
    th = (n%1000_000)//1000
    hu = (n%1000)
    if prefix == 'mi':
        prefix = 'i'
    str = ''
    if hu > 0:
        hu_str = hundreds_tens_units(prefix, hu)
        if (tr > 0) or (bi > 0) or (mi > 0) or (th > 0):
            hu_str = (' n\'' if (hu_str[0:1] in vowels) else ' na ') + hu_str
        str = hu_str + str
    if th > 0:
        th_str = thousands(th)
        if (tr > 0) or (bi > 0) or (mi > 0):
            th_str = ' n\'' + th_str
        str = th_str + str
    if mi > 0:
        mi_str = millions(mi)
        if (tr > 0) or (bi > 0):
            mi_str = ' na ' + mi_str
        str = mi_str + str
    if bi > 0:
        bi_str = billions(bi)
        if (tr > 0):
            bi_str = ' na ' + bi_str
        str = bi_str + str
    if tr > 0:
        tr_str = trillions(tr)
        str =  tr_str + str
    return str

