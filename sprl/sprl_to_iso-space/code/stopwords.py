# -*- coding: utf-8 -*-

import nltk

#substitute these for generic 'person' for word net similarity
sne_pronouns = ['i', 'me', 'you', 'he', 'she'
                'him', 'her', 'us', 'our', 'we',
                'my', 'your', 'yours', 'mine', 'ours'
                'his', 'hers', 'theirs', 'their', 'everyone'
                'everybody', 'who', 'whom', 'whose']

#substitute these for generic 'place' for word net similarity
loc_pronouns = ['where', 'there', 'here', 'yonder']

#substitute these for generic 'thing' for word net similarity
unknown_pronouns = ['other', 'both', 'some', 'that', 'it', 'this'
                   'those', 'these', 'what', 'which']

def sub(word):
    if word in sne_pronouns:
        return 'person'
    elif word in loc_pronouns:
        return 'location'
    elif word in unknown_pronouns:
        return 'thing'
    return word
