# -*- coding: utf-8 -*-
#from __future__ import unicode_literals, print_function

import codecs
import os
import sys
import unittest
import barcode

from barcode import get_barcode, get_barcode_class, __version__

print (barcode.PROVIDED_BARCODES)
#[u'code39', u'ean', u'ean13', u'ean8', u'gs1', u'gtin', u'isbn', u'isbn10',
# u'isbn13', u'issn', u'jan', u'pzn', u'upc', u'upca']
EAN = barcode.get_barcode_class('ean13')
#EAN
#<class 'barcode.ean.EuropeanArticleNumber13'>
ean = EAN(u'5901234123457')
#ean
#<barcode.ean.EuropeanArticleNumber13 object at 0x00BE98F0>
fullname = ean.save('picbarcode/ean13_barcode')
#fullname
#u'ean13_barcode.svg'
# Example with PNG
from barcode.writer import ImageWriter
ean = EAN(u'5901234123457', writer=ImageWriter())
fullname = ean.save('picbarcode/ean13_barcode')
#u'ean13_barcode.png'
# New in v0.4.2
from StringIO import StringIO
fp = StringIO()
ean.write(fp)
# or
f = open('picbarcode/file', 'wb')
ean.write(f) # PIL (ImageWriter) produces RAW format here
# New in v0.5.0
from barcode import generate
name = generate('EAN13', u'5901234123457', output='picbarcode/barcode_svg')
#name
#u'barcode_svg.svg'
# with file like object
fp = StringIO()
generate('EAN13', u'5901234123457', writer=ImageWriter(), output=fp)
