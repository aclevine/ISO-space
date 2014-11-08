# -*- coding: utf-8 -*-

"""
Code to evaluate an SPRL to ISO-Space tag transducer.
"""

import tagdoc as td
import classify as c

#iso text of document is one index ahead (an extra new line)
#therefore, to get correct offsets, use this formula
#iso_offset = sprl_offset + 1
#sprl_offset = iso_offset - 1
#e.g. iso.text[1016:1018] == sprl.txt[1015:1017]

TAG = 0
LABEL = 1

iso = td.TagDoc(td.ISO_FILE)
sne = iso.tagDict['SPATIAL_ENTITY']
place = iso.tagDict['PLACE']
path = iso.tagDict['PATH']

def eval1(tagnames=['TRAJECTOR', 'LANDMARK'], sprl=td.TagDoc(td.SPRL_FILE), iso=td.TagDoc(td.ISO_FILE)):
    """
    Evaluates classification of trajector and landmark tags.
    """
    tags = []
    for tagname in tagnames:
        tags += sprl.tagDict[tagname]
    classified = [(tag, c.classify(tag)[LABEL]) for tag in tags]
    iso_tags = {c[LABEL]: iso.tagDict[c[LABEL]] for c in classified}
    stats = {label: [] for label in iso_tags.keys()}
    for h in classified:
        sprl_tag = h[TAG]
        label = h[LABEL]
        for iso_tag in iso_tags[label]:
            sprl_start = int(sprl_tag.attrib['start'])
            sprl_end = int(sprl_tag.attrib['end'])
            iso_start = int(iso_tag.attrib['start']) - 20
            iso_end = int(iso_tag.attrib['end']) + 20
            if sprl_tag.attrib['text'] in sprl.text[iso_start:iso_end] and sprl_start >= iso_start and sprl_end <= iso_end:
                sprl_set = set(sprl_tag.attrib['text'].split())
                iso_set = set(iso_tag.attrib['text'].split())
                jaccard = 0
                try:
                    jaccard = len(sprl_set.intersection(iso_set)) / float(len(sprl_set.union(iso_set)))
                    stats[label].append((sprl_tag, iso_tag, jaccard, label))
                except ZeroDivisionError:
                    stats[label].append((sprl_tag, iso_tag, jaccard, label))
                    break
                break
    return stats
                    
                    
def summary(stats, isoDoc=td.TagDoc(td.ISO_FILE)):
    totals = {}
    score = {}
    for key in stats.keys():
        totals[key] = 0
        score[key] = 0
        for item in stats[key]:
            totals[key] += 1
            score[key] += float(item[-2])
    return (totals, score)
                


                    


        
        
    
    
    
    
    

