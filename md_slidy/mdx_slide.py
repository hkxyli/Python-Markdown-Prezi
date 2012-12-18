__author__ = 'Xiaoyang'
#!/usr/bin/env python
"""
Slide Extension for Python-Markdown
=============================================

Added parsing of slide to Python-Markdown.

A simple example:

    @Apple
    Pomaceous fruit of plants of the genus Malus in
    An american computer company.

    @Orange
       The fruit of an evergreen tree of the genus Citrus.

"""

import re
import markdown
from markdown.util import etree


class slideProcessor(markdown.blockprocessors.BlockProcessor):
    """ Process slide """
    RE = re.compile(r'(^|\n)@')# A block starts with @
    IS_1stBLock=True

    def test(self, parent, block):
        return bool(self.RE.match(block))

    def run(self, parent, blocks):
        block=blocks.pop(0)
        m=self.RE.match(block)
        if m :
            if not self.IS_fist_slide_block:
                block="</div>\n<div class='slide'>%s" % block[m.end():]
            else : #IS_fist_slide_block
                block="<div class='slide'>%s" % block[m.end():]
                self.IS_fist_slide_block=False
        blocks.append("</div>")

class slideExtension(markdown.Extension):
    """ Add definition lists to Markdown. """

    def extendMarkdown(self, md, md_globals):
        """ Add an instance of slideProcessor to BlockParser. """
        md.parser.blockprocessors.add('slide',
            slideProcessor(md.parser),
            '_begin')



def makeExtension(configs=None):
    return slideExtension(configs=configs)

