#This creates the main window of an application

class Character(object):
    def __init__(self):
        self.health = 100
 
class Blacksmith(Character):
    def __init__(self):
        super(Blacksmith, self).__init__()

class kriengten(object):
    def openpicture(self,aaa):
        import Tkinter as tk
        from PIL import ImageTk, Image
        window = tk.Tk()
        window.title("Join")
        window.geometry("300x300")
        window.configure(background='grey')
        window.winfo_toplevel
    #    path = "images.png"
        print aaa
        path = aaa
        #Creates a Tkinter-compatible photo image, which can be used everywhere Tkinter expects an image object.
        img = ImageTk.PhotoImage(Image.open(path))

        #The Label widget is a standard Tkinter widget used to display a text or image on the screen.
        panel = tk.Label(window, image = img)

        #The Pack geometry manager packs widgets in rows or columns.
        panel.pack(side = "bottom", fill = "both", expand = "yes")

        #Start the GUI
        window.mainloop()

    def openpicture2(self,aaa):
        from PIL import ImageTk, Image ,ImageDraw , ImageFont,ImageFile
        img =Image.open(aaa)
        img.show()

    def kbarcode(self,aaa):
        import codecs
        import os
        import sys
        import unittest
        import barcode
        from barcode import get_barcode, get_barcode_class, __version__
        print (barcode.PROVIDED_BARCODES)
        #[u'code39', u'ean', u'ean13', u'ean8', u'gs1', u'gtin', u'isbn', u'isbn10',
        # u'isbn13', u'issn', u'jan', u'pzn', u'upc', u'upca']
#        EAN = barcode.get_barcode_class('ean13')
        EAN = barcode.get_barcode_class('code39')
        #EAN
        #<class 'barcode.ean.EuropeanArticleNumber13'>

#        ean = EAN(u'5901234123457')

        #ean
        #<barcode.ean.EuropeanArticleNumber13 object at 0x00BE98F0>

#        fullname = ean.save('picbarcode/ean13_barcode')

        #fullname
        #u'ean13_barcode.svg'
        # Example with PNG
 
        from barcode.writer import ImageWriter
#        ean = EAN(u'5901234123457', writer=ImageWriter())
        uuu = unicode(aaa, "utf-8")
        ean = EAN(uuu, writer=ImageWriter())
#        ean = EAN(u'5901234123457', writer=ImageWriter())

#        fullname = ean.save('picbarcode/ean13_barcode')
 
        #u'ean13_barcode.png'
        # New in v0.4.2
#        from StringIO import StringIO
#        fp = StringIO()
#        ean.write(fp)
        # or
        f = open('picbarcode/file.png', 'wb')
        ean.write(f) # PIL (ImageWriter) produces RAW format here
        f.close
        # New in v0.5.0

#        from barcode import generate
#        name = generate('EAN13', u'5901234123457', output='picbarcode/barcode_svg')

        #name
        #u'barcode_svg.svg'
        # with file like object

#        fp = StringIO()
#        generate('EAN13', u'5901234123457', writer=ImageWriter(), output=fp)

#rootkri = tk()
#bs = Blacksmith()
#print (bs.health)
#c1=kriengten()
#c1.openpicture('images.png')