'''Meta command which generates the meta file'''

import yaml
import re
import os

from pathlib import Path, PosixPath
from logging import Logger
from foliant.meta_commands.base import BaseMetaCommand
from foliant.cli.meta.classes import Meta


YFM_PATTERN = re.compile(r'^\s*---(?P<yaml>.+?\n)---', re.DOTALL)
SECTION_PATTERN =\
    re.compile(r'^(?P<title>#+ .+?)\n\s*---\n(?P<yaml>(?:[^\n]+\n)*)---',
               re.MULTILINE)


def generate_meta(context: dict, logger: Logger):
    '''
    Helper function to generate meta.yml to be run from anywhere

    Returns meta filename (relative to project root).
    '''
    meta_command = MetaCommand(context, logger)
    meta_command.run()
    return Meta(meta_command.options['filename'])


def flatten_seq(seq):
    """convert a sequence of embedded sequences into a plain list"""
    result = []
    vals = seq.values() if type(seq) == dict else seq
    for i in vals:
        if type(i) in (dict, list):
            result.extend(flatten_seq(i))
        else:
            result.append(i)
    return result


class FlatChapters:
    """
    Helper class converting chapter list of complicated structure
    into a plain list of chapter names or path to actual md files
    in the src dir.
    """

    def __init__(self,
                 chapters: list,
                 parent_dir: PosixPath = Path('src')):
        self._chapters = chapters
        self._parent_dir = parent_dir

    def __len__(self):
        return len(self.flat)

    def __getitem__(self, ind: int):
        return self.flat[ind]

    def __contains__(self, item: str):
        return item in self.flat

    def __iter__(self):
        return iter(self.flat)

    @property
    def flat(self):
        """Flat list of chapter file names"""
        return flatten_seq(self._chapters)

    @property
    def list(self):
        """Original chapters list"""
        return self._chapters

    @property
    def paths(self):
        """Flat list of PosixPath objects relative to project root."""
        return (self._parent_dir / chap for chap in self.flat)


def get_yfm(content: str):
    '''Get YAML front matter from md-file content'''
    match = re.search(YFM_PATTERN, content)
    if match:
        return yaml.load(match.group('yaml'), yaml.Loader)
    else:
        return {}


def get_title(content: str, yfm: dict, ch_name: str):
    '''Return proper title of the main section:

    If field 'title' is in yfm — return its value;
    If not — return first heading of the document;
    If there are no headings — return the name of the file without extension.
    '''
    if 'title' in yfm:
        return yfm['title']

    pattern = re.compile(r'^#+\s+(.+)', re.MULTILINE)
    match = re.search(pattern, content)
    if match:
        return match.group(1)
    else:
        return Path(ch_name).stem


def get_meta_for_chapter(ch_name: str, content: str) -> dict:
    '''
    Get metadata for one chapter.

    Returns a chapter dictionary.
    '''
    chap_dict = {
        'chapter': ch_name,
        'yfm': get_yfm(content),
    }
    chap_dict['title'] = get_title(content,
                                   chap_dict['yfm'],
                                   ch_name)

    return chap_dict


class MetaCommand(BaseMetaCommand):
    '''Meta command which generates the meta file'''
    defaults = {'filename': 'meta.yml'}
    config_section = 'meta'

    def _gen_meta(self):
        '''Generate meta yaml and return it as string'''

        if 'chapters' not in self.config:
            return ''
        c = FlatChapters(self.config['chapters'])
        result = []
        for chap, path_ in zip(c.flat, c.paths):
            if not os.path.exists(path_):
                print(f"Can't find {path_}, meta for chapter not created")
                continue
            with open(path_, encoding='utf8') as f:
                content = f.read()
            chap_dict = get_meta_for_chapter(chap, content)
            result.append(chap_dict)
        return result

    def run(self):
        self.logger.debug('Meta command generate started')

        meta = self._gen_meta()
        with open(self.options['filename'], 'w', encoding='utf8') as f:
            yaml.dump(meta, f, default_flow_style=False, allow_unicode=True)

        self.logger.debug('Meta command generate finished')
