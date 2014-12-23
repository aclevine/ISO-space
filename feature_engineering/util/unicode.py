# -*- coding: utf-8 -*-

"""Code to replace unicode characters with corresponding ASCII characters.

.. moduleauthor:: Seth-David Donald Dworman <sdworman@brandeis.edu>

"""

u2ascii = {}
ureverse = {}

u2ascii[u'\u0103'] = 'a' #'ă'
u2ascii[u'\u2002'] = ' ' #unknown white space character

u2ascii[u'\u2013'] = '-' #'–'
u2ascii[u'\u2014'] = '-' #'—'

u2ascii[u'\u2019'] = '\'' #'’'

u2ascii[u'\u2018'] = '\'' #'‘'

u2ascii[u'\u201d'] = '"' #'”'

u2ascii[u'\u201c'] = '"' #'“'

u2ascii[u'\xa1'] = '!' #'¡'

u2ascii[u'\u2122'] = '' #'™'

u2ascii[u'\u2026'] = '' #'…'

u2ascii[u'\x9d'] = ' ' #''

u2ascii[u'\xad'] = ' ' #'­'

u2ascii[u'\u20ac'] = '$' #'€'

u2ascii[u'\xb0'] = ' ' #'°'

u2ascii[u'\xbf'] = '?' #'¿'

u2ascii[u'\xc1'] = 'A' #'Á'

u2ascii[u'\xc3'] = 'A' #'Ã'

u2ascii[u'\xc2'] = 'A' #'Â'

u2ascii[u'\u0153'] = 'o' #'œ'

u2ascii[u'\u02dc'] = '~' #'˜'

u2ascii[u'\u015f'] = 's' #'ş'

u2ascii[u'\xe1'] = 'a' #'á'

u2ascii[u'\u0163'] = 't' #'ţ'

u2ascii[u'\xe2'] = 'a' #'â'

u2ascii[u'\xe9'] = 'e' #'é'

u2ascii[u'\xed'] = 'i' #'í'

u2ascii[u'\xee'] = 'i' #'î'

u2ascii[u'\xf1'] = 'n' #'ñ'

u2ascii[u'\xf3'] = 'o' #'ó'

u2ascii[u'\xf6'] = 'o' #'ö'

u2ascii[u'\xfc'] = 'u' #'ü'

u2ascii[u'\xb4'] = '\'' #´

u2ascii[u'\xdf'] = 's' #ß

ureverse = {u2ascii[key]:key for key in u2ascii}

def ureplace(text, reverse=False):
    return ''.join([char if ord(char) < 128 else u2ascii[char] for char in text])

