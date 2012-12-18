__author__ = 'Xiaoyang'

import re
import markdown
from markdown.util import etree

class slideTreeProcessor(markdown.treeprocessors.Treeprocessor):
    """ Process slide """

    def run (self, root):
        print "root"
        return root

class slideTreeProcessor(markdown.Extension):
    """ Add definition lists to Markdown. """

    def extendMarkdown(self, md, md_globals):
        """ Add an instance of slideProcessor to BlockParser. """
        md.treeprocessors.add('tree',
            slideTreeProcessor(md.parser),
            '_begin')

def makeExtension(configs=None):
    return slideTreeProcessor(configs=configs)

