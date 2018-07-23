#! /usr/bin/env python
# -*- coding: utf-8 -*-
#this code is develop follow jane code for opensource user and programmer
# 2018-07-18 (Y-m-d)
# apt-get install pcscd python-pyscard
from reportlab.pdfgen import canvas
import subprocess, sys
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('THSarabunNew','THSarabunNew.ttf'))

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
    kid.append(",")
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
    kid.append(",")
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
    kid.append(",")
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
    kid.append(",")
    
    f1 = open('./kriid.txt','w+')
    for item in kid:
#        f1.write("%s" %item.strip())
        f1.write("%s" %item)
    f1.close
    print "Command8: %02X %02X" % (sw1, sw2)

def copytocsv():
        with open('./kriid.txt', 'r') as myfile:
            data=myfile.readline()
            list=data.split(",")
            id13=list[0]
            words = list[1].split("#")
            pre = words[0]
            name = words[1]
            uniline22 = words[3].split()
            surname = uniline22[0]
            uniline6 = words[6].split()
            uniline66 = uniline6[1]
            birth = uniline66[0:8]
            sex = uniline66[-1]
            words = list[2].split("#")
            address1 = words[0]+words[1]
            tumbon = words[5]
            amphur = words[6]
            province = words[7]
            f1 = open('./kriid.csv','w+')
            f1.write(id13+","+pre+name+" "+surname+","+birth+","+sex+","+address1+","+tumbon+","+amphur+","+province)
            f1.close
 

def printkri():
#from reportlab.pdfgen import canvas
        c = canvas.Canvas("hello.pdf")
        c.setFont('THSarabunNew', 16)
        with open('./kriid.txt', 'r') as myfile:
            data=myfile.readline()
            list=data.split(",")
            word=list[0]
        c.drawString(10,800,"ID บัตรประชาชน :")
        c.drawString(150,800,list[0])
        c.drawString(10,750,"ชื่อ - นามสกุล :")
        words = list[1].split("#")
        uniline0 = unicode(words[0],'cp874')
        uniline1 = unicode(words[1],'cp874')
        uniline2 = unicode(words[3],'cp874')
        uniline22 = uniline2.split()
        uniline6 = unicode(words[6],'cp874')
        uniline66 = uniline6.split()
        c.drawString(150,750,uniline0+" "+uniline1+" "+uniline22[0])
        c.drawString(10,700,"วันเดือนปีเกิด(YYYYMMDD) :")
        birth = uniline66[1]
        c.drawString(150,700,birth[0:8])
        c.drawString(10,650,"เพศ :")
        sex1 = birth[-1]
        if sex1 == '1':
            sex = "ชาย"
        if sex1 == '2':
            sex = "หญิง"
        
        c.drawString(150,650,sex)
        c.drawString(10,600,"ที่อยู่ :")
        words = list[2].split("#")
        uniline0 = unicode(words[0],'cp874')
        uniline1 = unicode(words[1],'cp874')
        uniline2 = unicode(words[5],'cp874')
        uniline3 = unicode(words[6],'cp874')
        uniline4 = unicode(words[7],'cp874')
        c.drawString(150,600,uniline0+" "+uniline1+" "+uniline2+" "+uniline3+" "+uniline4)
        c.drawString(10,500,"วันหมดอายุ :")
        c.drawString(150,500,list[3])
        c.save()
#import subprocess, sys
        opener ="open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, "hello.pdf"])


#from Tkinter import *
from Tkinter import Tk, Button, Frame, Entry,Label, END
from smartcard.System import readers
import binascii

root=Tk()  #It is just a holder

Label(root,text="Enter your name").grid(row=7,column=1) #Creating label
a=Entry(root)           #creating entry box
#a.grid(row=1,column=8)
a.grid(row=7,column=4)
Button(root,text="OK",command=xyz).grid(row=7,column=6)
Button(root,text="read idcard to txt",command=readcard).grid(row=1,column=1)
Button(root,text="copy to csv",command=copytocsv).grid(row=1,column=4)
Button(root,text="พิมพ์ ใบสมัครงาน",command=printkri).grid(row=1,column=6)

root.mainloop() 