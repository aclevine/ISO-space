import os
from corpus import *

"""A script to update XMLs annotated under ISO-Space-1.11 DTD to the SpaceEvalTask1.2 DTD."""

corpus_dir = os.path.join(
    os.environ['HOME'],
    'Dropbox/ISO-Space/SemEval/Test/update/RFC.ISOSpaceTaskv1.11'
)

update_dir = os.path.join(
    os.environ['HOME'],
    'Dropbox/ISO-Space/SemEval/Test/update/RFC.SpaceEvalTaskv1.2'
)

def main():
    for document in list(Corpus(corpus_dir).documents()):
        if document.task == 'ISOSpaceTaskv1.11':
            print document.basename
            document.rename_task('SpaceEvalTaskv1.2')
            # EVENT -> NONMOTION_EVENT
            document.rename_tag('EVENT', 'NONMOTION_EVENT')
            # PLACE, PATH, SPATIAL_ENTITY, NONMOTION_EVENT, MOTION :
            #   +attr : domain
            document.add_attribute(
                'domain',
                ttypes=(
                    'PLACE',
                    'PATH',
                    'SPATIAL_ENTITY',
                    'NONMOTION_EVENT',
                    'MOTION'
                )
            )
            # PATH :
            #   +attr : dcl
            document.add_attribute('dcl', value=u'FALSE', ttypes=('PATH'))
            # MOTION :
            #   +attrs : latlong, elevation
            for attr in ('latlong', 'elevation'):
                document.add_attribute(attr, ttypes=('MOTION'))
            # ADJUNCT -> MOTION_SIGNAL :
            #   %attr : adjunct_type -> motion_signal_type
            document.rename_tag('ADJUNCT', 'MOTION_SIGNAL')
            document.rename_attribute(
                'adjunct_type',
                'motion_signal_type',
                ttypes=('MOTION_SIGNAL')
            )        
            # MLINK -> MEASURELINK :
            document.rename_tag('MLINK', 'MEASURELINK')
            # MEASURELINK, MOVELINK, OLINK, QSLINK :
            #   %attrs : figure -> trajector, ground -> landmark
            for old, new in zip(('figure', 'ground'), ('trajector', 'landmark')):
                document.rename_attribute(
                    old,
                    new,
                    ttypes=['MEASURELINK', 'MOVELINK', 'OLINK', 'QSLINK']
                )
            document.save_xml(os.path.join(update_dir, document.basename))

if __name__ == '__main__':
    main()
