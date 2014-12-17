__author__ = "Zachary Yocum"
__email__ = "zyocum@brandeis.edu"

import corpus, re, shutil
from warnings import warn

home = os.environ['HOME']
base_path = os.path.join(home, 'Dropbox', 'ISO-Space', 'Annotation')
os.chdir(base_path)
corpora_path, corpora, other_files = os.walk(os.getcwd()).next()
with open('Annotators.txt', 'r') as file:
    lines = file.read().strip().split('\n')
    annotator = lambda name, initials, identifier : {
        'name' : name,
        'initals' : initials,
        'id' : identifier
    }
    parse = lambda l : l.split(' : ')
    annotators = map(lambda l : annotator(*parse(l)), lines)

corpus = 'ANC'
text = 'WhereToJapan'
text_path = os.path.join(base_path, corpus, 'Adjudication', text)

annotators = ['A20', 'A22']
pattern = '(?P<text>{t})_(?P<section>.+)-(?P<annotator>[Aa][0-9]+)-(?P<phase>[Pp][0-9]+).xml'.format(t=text)

def get_section(xml):
    """Attempt to determine the section that an XML annotation file belongs to based on the file name."""
    xml = unicode(xml, encoding='utf-8')
    match = re.match(re.compile(pattern, re.U), xml)
    if match:
        return match.group('section')
    else:
        message = "Failed to get section for '{s}".format(s=xml)
        warn(message, RuntimeWarning)
        return None

def make_dir(dir):
    """Create a directory at the given location if it doesn't already exist."""
    if not os.path.exists(dir):
        os.makedirs(dir)

def run(annotators=annotators, path=path, pattern=pattern):
    """Find all XML annotation files for each annotator and copy them into directories for the sections they belong to."""
    # loop over each annotator
    for annotator in annotators:
        annotator_dir = os.sep.join([path, annotator])
        # compile a list of xml annotation file names based on regex pattern matching
        xmls = filter(
            lambda f : re.match(
                re.compile(pattern, re.U), unicode(f, encoding='utf-8')
            ),
            os.listdir(annotator_dir)
        )
        # loop over each of the xml annotation file names
        for xml in xmls:
            # find which section the file belongs to
            section = get_section(xml).encode('utf-8')
            # create a directory for the seciton if one doesn't exist
            make_dir(os.sep.join([path, section]))
            # determine the file to be copied
            source = os.sep.join([annotator_dir, xml])
            # determine the destination to copy the file to
            destination = os.sep.join([path, section, xml])
            # copy the file
            shutil.copy(source, destination)

if __name__ == '__main__':
    run()
