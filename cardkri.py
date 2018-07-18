#! /usr/bin/env python
#this code is develop follow jane code for opensource user and programmer
# 2018-07-18 (Y-m-d)
# apt-get install pcscd python-pyscard

def xyz():
    global a
    print a.get() 

def readcard():
# Thailand ID Smartcard
# define the APDUs used in this script
# Reset
    SELECT = [0x00, 0xA4, 0x04, 0x00, 0x08, 0xA0, 0x00, 0x00, 0x00, 0x54, 0x48, 0x00, 0x01]
# CID
    COMMAND1 = [0x80, 0xb0, 0x00, 0x04, 0x02, 0x00, 0x0d]
    COMMAND2 = [0x00, 0xc0, 0x00, 0x00, 0x0d]
# Fullname Thai + Eng + BirthDate + Sex
    COMMAND3 = [0x80, 0xb0, 0x00, 0x11, 0x02, 0x00, 0xd1]
    COMMAND4 = [0x00, 0xc0, 0x00, 0x00, 0xd1]
# Address
    COMMAND5 = [0x80, 0xb0, 0x15, 0x79, 0x02, 0x00, 0x64]
    COMMAND6 = [0x00, 0xc0, 0x00, 0x00, 0x64]
# issue/expire
    COMMAND7 = [0x80, 0xb0, 0x01, 0x67, 0x02, 0x00, 0x12]
    COMMAND8 = [0x00, 0xc0, 0x00, 0x00, 0x12]
# get all the available readers
    r = readers()
    print "Available readers:", r
    reader = r[0]
    print "Using:", reader
    connection = reader.createConnection()
    connection.connect()
# Reset
    data, sw1, sw2 = connection.transmit(SELECT)
    print data
    print "Select Applet: %02X %02X" % (sw1, sw2)
    data, sw1, sw2 = connection.transmit(COMMAND1)
    print data
    print "Command1: %02X %02X" % (sw1, sw2)
#print "Command1 kri : %02X " % (sw1)
# CID
    data, sw1, sw2 = connection.transmit(COMMAND2)
    print data
    print "testkri %s" % (data)
    kid = []
    for d in data:
        kid.append(chr(d))
        print chr(d),
    print
#print kid
    kid.append(":")
    print "Command2: %02X %02X" % (sw1, sw2)
 
# Fullname Thai + Eng + BirthDate + Sex
    data, sw1, sw2 = connection.transmit(COMMAND3)
    print data
    print "Command3: %02X %02X" % (sw1, sw2)
 
    data, sw1, sw2 = connection.transmit(COMMAND4)
    print data
    for d in data:
        kid.append(chr(d))
        print unicode(chr(d),"tis-620"),
    print
    kid.append(":")
    print "Command4: %02X %02X" % (sw1, sw2)
 
# Address
    data, sw1, sw2 = connection.transmit(COMMAND5)
    print data
    print "Command5: %02X %02X" % (sw1, sw2)
 
    data, sw1, sw2 = connection.transmit(COMMAND6)
    print data
    for d in data:
        kid.append(chr(d))
        print unicode(chr(d),"tis-620"),
    print
    kid.append(":")
    print "Command6: %02X %02X" % (sw1, sw2)
 
# issue/expire
    data, sw1, sw2 = connection.transmit(COMMAND7)
    print data
    print "Command7: %02X %02X" % (sw1, sw2)
 
    data, sw1, sw2 = connection.transmit(COMMAND8)
    print data
    for d in data:
        kid.append(chr(d))
        print unicode(chr(d),"tis-620"),
    print
    kid.append(":")
    f1 = open('./kriid.txt','w+')
    for item in kid:
        f1.write("%s" %item)
    f1.close
    print "Command8: %02X %02X" % (sw1, sw2)

#from Tkinter import *
from Tkinter import Tk, Button, Frame, Entry,Label, END
from smartcard.System import readers
import binascii

root=Tk()  #It is just a holder

Label(root,text="Enter your name").grid(row=7,column=1) #Creating label
a=Entry(root)           #creating entry box
#a.grid(row=1,column=8)
a.grid(row=7,column=8)
Button(root,text="OK",command=xyz).grid(row=4,column=1)
Button(root,text="write id card data to file",command=readcard).grid(row=1,column=1)

root.mainloop() 