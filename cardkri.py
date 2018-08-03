#! /usr/bin/env python
# -*- coding: utf-8 -*-
#this code is develop follow jane code for opensource user and programmer
# 2018-07-18 (Y-m-d)
# apt-get install pcscd python-pyscard
# from Tkinter import *
from Tkinter import Tk, Button, Frame, Entry,Label,StringVar
import Tkinter as tk
import io, binascii,shutil,datetime,time
import subprocess, sys , os ,MySQLdb ,mysql.connector
from time import sleep
#from datetime import date,time,timedelta
from PIL import ImageTk, Image ,ImageDraw , ImageFont,ImageFile
from smartcard.System import readers
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from tkFileDialog import askopenfilename
from mysql.connector import MySQLConnection, Error
from krieng import read_kri_config,read_db_config
from smartcard.util import HexListToBinString, toHexString, toBytes
from picturekri import kriengten

pdfmetrics.registerFont(TTFont('THSarabunNew','THSarabunNew.ttf'))
db_config = read_db_config()

def readcard():
    initkri()
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
    f1 = open('./kriid.txt','r')
    data=f1.readline()
    list=data.split(",")
    id13=list[0]
    words = list[1].split("#")
    pre = words[0]
    name = words[1]
    surname = words[3].split()[0]
    birth = words[6].split()[1][0:8]
    sex = words[6].split()[1][-1]
    if sex=='1':
        kripre = '1'
    if sex=='2':
        if unicode(pre,"tis-620") == u'น.ส.' or unicode(pre,"tis-620") == u'ด.ญ.':
            kripre='2'
        else:
            kripre='3'    
    words = list[2].split("#")
    address1 = words[0]+words[1]
    tumbon0 = words[5]
    thaitumbon = unicode(tumbon0,"tis-620")
    tumbon1 = thaitumbon.replace(u'ตำบล',"")
    tumbon = tumbon1.encode('tis-620')
    amphur0 = words[6]
    thaiamphur = unicode(amphur0,"tis-620")
    amphur1 = thaiamphur.replace(u'อำเภอ',"")
    amphur = amphur1.encode('tis-620')
    province0 = words[7].strip()
    print province0
    print unicode(province0,"tis-620")
    thaiprovince = unicode(province0,"tis-620")
    province1 = thaiprovince.replace(u'จังหวัด',"")
    province = province1.encode('tis-620')
    expire = list[3]
    f1.close
    csvfile = '../Dropbox/krifoxone/kriid.csv'
    if os.path.isfile(csvfile):
        f1 = open(csvfile,'w+')
        f1.write(id13+","+pre+name+" "+surname+","+birth+","+sex+","+address1+","+tumbon+","+amphur+","+province+","+name+","+surname+","+kripre+","+expire)
        f1.close
        sv = StringVar(root,value='เริ่ม อ่านบัตร')
        print "start cardreader"
        a=Entry(root,textvariable=sv)           #creating entry box
        a.grid(row=5,column=1)
        sv1 = StringVar(root,value="HN")
        aa=Entry(root,textvariable=sv1)           #creating entry box
        aa.grid(row=5,column=6)
        print "HN"
        cardname = pre+name+" "+surname
        cardname2 = unicode(cardname,'tis-620')
        Label(root,text=cardname2).grid(row=1,column=8) #Creating label
        abirth = int(birth)
        abirth2 = abirth%100
        abirth3 = int(abirth/100%100)
        abirth4 = int(abirth/10000%10000)
        Label(root,text=" ("+str(abirth4)+") "+str(abirth4-543)+"-"+str(abirth3)+"-"+str(abirth2)+"  ").grid(row=5,column=8) #Creating label

    else:
        print("ไม่พบ file kriid.csv")
        sv = StringVar(root,value='เปิด cardkri.py ผิดที่')
        print "start cardreader"
        a=Entry(root,textvariable=sv)           #creating entry box
        a.grid(row=5,column=1)
        sv1 = StringVar(root,value="HN")
        aa=Entry(root,textvariable=sv1)           #creating entry box
        aa.grid(row=5,column=6)
        print "HN"

#def getData(self,cmd, req = [0x00, 0xc0, 0x00, 0x00]):
#def getData(cmd, req):
#	data, sw1, sw2 = self.connection.transmit(cmd)
#	data, sw1, sw2 = connection.transmit(req + [cmd[-1]])
#	data, sw1, sw2 = self.connection.transmit(req + [cmd[-1]])
#	return [data, sw1, sw2]
def thai2unicode(data):
	result = ''
	if isinstance(data, list):
		for d in data:
			result += unicode(chr(d),"tis-620")
	else :
		result = data.decode("tis-620").encode("utf-8")
	return result.strip()

def photoid13():
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
# Photo_Part1-20
    req1 = [0x00, 0xc0, 0x00, 0x00]
    CMD_PHOTO1 = [0x80, 0xb0, 0x01, 0x7B, 0x02, 0x00, 0xFF]
    CMD_PHOTO2 = [0x80, 0xb0, 0x02, 0x7A, 0x02, 0x00, 0xFF]
    CMD_PHOTO3 = [0x80, 0xb0, 0x03, 0x79, 0x02, 0x00, 0xFF]
    CMD_PHOTO4 = [0x80, 0xb0, 0x04, 0x78, 0x02, 0x00, 0xFF]
    CMD_PHOTO5 = [0x80, 0xb0, 0x05, 0x77, 0x02, 0x00, 0xFF]
    CMD_PHOTO6 = [0x80, 0xb0, 0x06, 0x76, 0x02, 0x00, 0xFF]
    CMD_PHOTO7 = [0x80, 0xb0, 0x07, 0x75, 0x02, 0x00, 0xFF]
    CMD_PHOTO8 = [0x80, 0xb0, 0x08, 0x74, 0x02, 0x00, 0xFF]
    CMD_PHOTO9 = [0x80, 0xb0, 0x09, 0x73, 0x02, 0x00, 0xFF]
    CMD_PHOTO10 = [0x80, 0xb0, 0x0A, 0x72, 0x02, 0x00, 0xFF]
    CMD_PHOTO11 = [0x80, 0xb0, 0x0B, 0x71, 0x02, 0x00, 0xFF]
    CMD_PHOTO12 = [0x80, 0xb0, 0x0C, 0x70, 0x02, 0x00, 0xFF]
    CMD_PHOTO13 = [0x80, 0xb0, 0x0D, 0x6F, 0x02, 0x00, 0xFF]
    CMD_PHOTO14 = [0x80, 0xb0, 0x0E, 0x6E, 0x02, 0x00, 0xFF]
    CMD_PHOTO15 = [0x80, 0xb0, 0x0F, 0x6D, 0x02, 0x00, 0xFF]
    CMD_PHOTO16 = [0x80, 0xb0, 0x10, 0x6C, 0x02, 0x00, 0xFF]
    CMD_PHOTO17 = [0x80, 0xb0, 0x11, 0x6B, 0x02, 0x00, 0xFF]
    CMD_PHOTO18 = [0x80, 0xb0, 0x12, 0x6A, 0x02, 0x00, 0xFF]
    CMD_PHOTO19 = [0x80, 0xb0, 0x13, 0x69, 0x02, 0x00, 0xFF]
    CMD_PHOTO20 = [0x80, 0xb0, 0x14, 0x68, 0x02, 0x00, 0xFF]
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
# CID
    data, sw1, sw2 = connection.transmit(COMMAND2)
    print data
    print "testkri %s" % (data)
    kid = []
#    kid2= []
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
    photo = []
    data, sw1, sw2 = connection.transmit(CMD_PHOTO1)
    data, sw1, sw2 = connection.transmit(req1 + [CMD_PHOTO1[-1]])
    photo += data
    data, sw1, sw2 = connection.transmit(CMD_PHOTO2)
    data, sw1, sw2 = connection.transmit(req1 + [CMD_PHOTO2[-1]])
    photo += data
    data, sw1, sw2 = connection.transmit(CMD_PHOTO3)
    data, sw1, sw2 = connection.transmit(req1 + [CMD_PHOTO3[-1]])
    photo += data
    data, sw1, sw2 = connection.transmit(CMD_PHOTO4)
    data, sw1, sw2 = connection.transmit(req1 + [CMD_PHOTO4[-1]])
    photo += data
    data, sw1, sw2 = connection.transmit(CMD_PHOTO5)
    data, sw1, sw2 = connection.transmit(req1 + [CMD_PHOTO5[-1]])
    photo += data
    data, sw1, sw2 = connection.transmit(CMD_PHOTO6)
    data, sw1, sw2 = connection.transmit(req1 + [CMD_PHOTO6[-1]])
    photo += data
    data, sw1, sw2 = connection.transmit(CMD_PHOTO7)
    data, sw1, sw2 = connection.transmit(req1 + [CMD_PHOTO7[-1]])
    photo += data
    data, sw1, sw2 = connection.transmit(CMD_PHOTO8)
    data, sw1, sw2 = connection.transmit(req1 + [CMD_PHOTO8[-1]])
    photo += data
    data, sw1, sw2 = connection.transmit(CMD_PHOTO9)
    data, sw1, sw2 = connection.transmit(req1 + [CMD_PHOTO9[-1]])
    photo += data
    data, sw1, sw2 = connection.transmit(CMD_PHOTO10)
    data, sw1, sw2 = connection.transmit(req1 + [CMD_PHOTO10[-1]])
    photo += data
    data, sw1, sw2 = connection.transmit(CMD_PHOTO11)
    data, sw1, sw2 = connection.transmit(req1 + [CMD_PHOTO11[-1]])
    photo += data
    data, sw1, sw2 = connection.transmit(CMD_PHOTO12)
    data, sw1, sw2 = connection.transmit(req1 + [CMD_PHOTO12[-1]])
    photo += data
    data, sw1, sw2 = connection.transmit(CMD_PHOTO13)
    data, sw1, sw2 = connection.transmit(req1 + [CMD_PHOTO13[-1]])
    photo += data
    data, sw1, sw2 = connection.transmit(CMD_PHOTO14)
    data, sw1, sw2 = connection.transmit(req1 + [CMD_PHOTO14[-1]])
    photo += data
    data, sw1, sw2 = connection.transmit(CMD_PHOTO15)
    data, sw1, sw2 = connection.transmit(req1 + [CMD_PHOTO15[-1]])
    photo += data
    data, sw1, sw2 = connection.transmit(CMD_PHOTO16)
    data, sw1, sw2 = connection.transmit(req1 + [CMD_PHOTO16[-1]])
    photo += data
    data, sw1, sw2 = connection.transmit(CMD_PHOTO17)
    data, sw1, sw2 = connection.transmit(req1 + [CMD_PHOTO17[-1]])
    photo += data
    data, sw1, sw2 = connection.transmit(CMD_PHOTO18)
    data, sw1, sw2 = connection.transmit(req1 + [CMD_PHOTO18[-1]])
    photo += data
    data, sw1, sw2 = connection.transmit(CMD_PHOTO19)
    data, sw1, sw2 = connection.transmit(req1 + [CMD_PHOTO19[-1]])
    photo += data
    data, sw1, sw2 = connection.transmit(CMD_PHOTO20)
    data, sw1, sw2 = connection.transmit(req1 + [CMD_PHOTO20[-1]])
    photo += data
    dataa1 = HexListToBinString(photo)
    f1 = open('./kriid.txt','r')
    data=f1.readline()
    list=data.split(",")
    id13=list[0]
    expire=list[3]
    kripic =id13+expire+".jpg"
    f = open(kripic, "wb")
    f.write(dataa1)
    f.flush()
    f.close
    sleep(0.1)
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    f_src = open(id13+expire+".jpg",'rb')
    f_dest = open("images.jpg",'wb')
    shutil.copyfileobj(f_src,f_dest)
    sleep(0.1)
    imgkri(kripic)
    words = list[1].split("#")
    pre = words[0]
    name = words[1]
#    uniline22 = words[3].split()
#    surname = uniline22[0]
    surname = words[3].split()[0]
#    uniline6 = words[6].split()
#    uniline66 = uniline6[1]
#    birth = uniline66[0:8]
    birth = words[6].split()[1][0:8]
#    sex = uniline66[-1]
    sex = words[6].split()[1][-1]
    if sex=='1':
        kripre = '1'
    if sex=='2':
        if unicode(pre,"tis-620") == u'น.ส.' or unicode(pre,"tis-620") == u'ด.ญ.':
            kripre='2'
        else:
            kripre='3'    
    words = list[2].split("#")
    address1 = words[0]+words[1]
    tumbon0 = words[5]
#    tumbon = tumbon0[4:30] #  amphur = amphur0[5:30] #  province = province0[7:30]
    thaitumbon = unicode(tumbon0,"tis-620")
    tumbon1 = thaitumbon.replace(u'ตำบล',"")
    tumbon = tumbon1.encode('tis-620')
    amphur0 = words[6]
    thaiamphur = unicode(amphur0,"tis-620")
    amphur1 = thaiamphur.replace(u'อำเภอ',"")
    amphur = amphur1.encode('tis-620')
    province0 = words[7].strip()
    print unicode(province0,"tis-620")
    thaiprovince = unicode(province0,"tis-620")
    province1 = thaiprovince.replace(u'จังหวัด',"")
    province = province1.encode('tis-620')
    f1.close
    csvfile = '../Dropbox/krifoxone/kriid.csv'
    if os.path.isfile(csvfile):
        f1 = open(csvfile,'w+')
        f1.write(id13+","+pre+name+" "+surname+","+birth+","+sex+","+address1+","+tumbon+","+amphur+","+province+","+name+","+surname+","+kripre+","+expire)
        f1.close
        sv = StringVar(root,value='เริ่ม อ่านบัตร')
        print "start cardreader"
        a=Entry(root,textvariable=sv)           #creating entry box
        a.grid(row=5,column=1)
        sv1 = StringVar(root,value="HN")
        aa=Entry(root,textvariable=sv1)           #creating entry box
        aa.grid(row=5,column=6)
        print "HN"
        cardname = pre+name+" "+surname
        cardname2 = unicode(cardname,'tis-620')
        Label(root,text=cardname2).grid(row=1,column=8) #Creating label
        abirth = int(birth)
        abirth2 = abirth%100
        abirth3 = int(abirth/100%100)
        abirth4 = int(abirth/10000%10000)
        Label(root,text=" ("+str(abirth4)+") "+str(abirth4-543)+"-"+str(abirth3)+"-"+str(abirth2)+"  ").grid(row=5,column=8) #Creating label
    else:
        print("ไม่พบ file kriid.csv")
        sv = StringVar(root,value='เปิด cardkri.py ผิดที่')
        print "start cardreader"
        a=Entry(root,textvariable=sv)           #creating entry box
        a.grid(row=5,column=1)
        sv1 = StringVar(root,value="HN")
        aa=Entry(root,textvariable=sv1)           #creating entry box
        aa.grid(row=5,column=6)
        print "HN"



def copytocsv():
    '''
        with open('./kriid.txt', 'r') as myfile:
            data=myfile.readline()
            list=data.split(",")
            id13=list[0]
            words = list[1].split("#")
            f1 = open('../Dropbox/krifoxone/kriid.csv','w+')
            f1.write(id13+","+pre+name+" "+surname+","+birth+","+sex+","+address1+","+tumbon+","+amphur+","+province)
            f1.close
    '''
    sv = StringVar(root,value='copy เรียบร้อย')
    a=Entry(root,textvariable=sv)           #creating entry box
    a.grid(row=5,column=1)
    print "Copy Ready"
#    time.sleep(100)

def searchid13():
    global aa2
    aaa = aa2.get()
    print aaa 
    if aaa.isdigit():
        print "is number"
    else:
        print "is not number"
        sv1 = StringVar(root,value="ต้องใส่ตัวเลขเท่านั้น")
        aa=Entry(root,textvariable=sv1)           #creating entry box
        aa.grid(row=5,column=6)
        initkri()
        return

    if len(aaa)<> 13:
                    print "ใส่เลขไม่ครบ 13 หลัก"
                    sv1 = StringVar(root,value="ใส่เลขไม่ครบ 13 หลัก")
                    aa=Entry(root,textvariable=sv1)           #creating entry box
                    aa.grid(row=5,column=6)
                    return
    
    khn2 = ""
    try:
        print db_config
        print('Connecting to MySQL database...')
        conn = MySQLConnection(**db_config)
#conn = MySQLdb.connect(charset='utf8', init_command='SET NAMES UTF8')
        print('Connection Successful!!!')
        cursor = conn.cursor ()
        cursor.execute ("SELECT hn,name,surname,xn,brdate,id13 FROM krieng where trim(xn)<>'old' and id13='"+aaa.strip()+"';")
        acount = 0
        while True:
            rows = cursor.fetchmany ()
            if not rows:
                cursor.close ()
                conn.close ()
                if acount == 0:
                    print "ไม่พบid13 นี้"
                    sv1 = StringVar(root,value="ไม่พบid13 นี้")
                    aa=Entry(root,textvariable=sv1)           #creating entry box
                    aa.grid(row=5,column=6)
                    initkri()
                if acount >= 2:
                    print "มีid13 จำนวน"+str(acount)
                    sv1 = StringVar(root,value="มีid13 จำนวน"+str(acount))
                    aa=Entry(root,textvariable=sv1)           #creating entry box
                    aa.grid(row=5,column=6)
                break
            for row in rows:
                khn = row[0]
                khn2 = khn2+","+str(khn)
                print "HN =:", row[0]
                sv1 = StringVar(root,value=khn)
                aa=Entry(root,textvariable=sv1)           #creating entry box
                aa.grid(row=5,column=6)
#                Label(root,text=aaa.strip()).grid(row=5,column=4) #Creating label
                Label(root,text=row[5]).grid(row=12,column=6) #Creating label
                sv3 = StringVar(root,value=khn2)
                aa3=Entry(root,textvariable=sv3)           #creating entry box
                aa3.grid(row=6,column=6)
                sv4 = StringVar(root,value=row[1]+" "+row[2])
                aa4=Entry(root,textvariable=sv4)           #creating entry box
                aa4.grid(row=7,column=1)
                sv5 = StringVar(root,value='XN:'+row[3])
                aa5=Entry(root,textvariable=sv5)           #creating entry box
                aa5.grid(row=7,column=4)
                sv6 = StringVar(root,value=str(row[4]))
                aa6=Entry(root,textvariable=sv6)           #creating entry box
                aa6.grid(row=7,column=6)
                print khn
                print row[1]+" "+row[2]
                acount += 1
                print acount

    except Exception as e:
        print (e)
        sv1 = StringVar(root,value="ไม่สามารถเชื่อม mysql ได้")
        aa=Entry(root,textvariable=sv1)           #creating entry box
        aa.grid(row=5,column=6)
        print "ไม่สามารถเชื่อม mysql ได้"
    except :
        print("Unknow error occured")

def copyandfindid13():
    khn2 = ""
    try:
        print('Connecting to MySQL database...')
        print db_config
        conn = MySQLConnection(**db_config)
        print('Connection Successful!!!')
        cursor = conn.cursor ()
        myfile = open('./kriid.txt','r')
        data=myfile.readline()
        list=data.split(",")
        kid13=list[0]
        print kid13
        cursor.execute ("SELECT hn,name,surname,xn,brdate,id13 FROM krieng where id13='"+kid13+"';")
        acount = 0
        while True:
#            row = cursor.fetchone ()
            rows = cursor.fetchmany ()
            if not rows:
                cursor.close ()
                conn.close ()
                if acount == 0:
                    print "ไม่พบid13 นี้"
                    sv1 = StringVar(root,value="ไม่พบid13 นี้")
                    aa=Entry(root,textvariable=sv1)           #creating entry box
                    aa.grid(row=5,column=6)
                if acount >= 2:
                    print "มีid13 จำนวน"+str(acount)
                    sv1 = StringVar(root,value="มีid13 จำนวน"+str(acount))
                    aa=Entry(root,textvariable=sv1)           #creating entry box
                    aa.grid(row=5,column=6)
                sv = StringVar(root,value='copy เรียบร้อย')
                a=Entry(root,textvariable=sv)           #creating entry box
                a.grid(row=5,column=1)
                print "Copy Ready"
                break
            for row in rows:
#            if row is None and acount>0:   # row ==None
                khn = row[0]
                khn2 = khn2+","+str(khn)
                print "HN =:", row[0]
                sv1 = StringVar(root,value=khn)
                aa=Entry(root,textvariable=sv1)           #creating entry box
                aa.grid(row=5,column=6)
                Label(root,text=kid13).grid(row=5,column=4) #Creating label
#                sv2 = StringVar(root,value=kid13)
#                aa2=Entry(root,textvariable=sv2)           #creating entry box
#                aa2.grid(row=6,column=1)
                sv3 = StringVar(root,value=khn2)
                aa3=Entry(root,textvariable=sv3)           #creating entry box
                aa3.grid(row=6,column=6)
                sv4 = StringVar(root,value=row[1]+" "+row[2])
                aa4=Entry(root,textvariable=sv4)           #creating entry box
                aa4.grid(row=7,column=1)
                sv5 = StringVar(root,value='XN:'+row[3])
                aa5=Entry(root,textvariable=sv5)           #creating entry box
                aa5.grid(row=7,column=4)
                sv6 = StringVar(root,value=str(row[4]))
                aa6=Entry(root,textvariable=sv6)           #creating entry box
                aa6.grid(row=7,column=6)
                print khn
                print row[1]+" "+row[2]
#            +" "+row[2]
            acount += 1
    except Exception as e:
        print (e)
        sv1 = StringVar(root,value="ไม่สามารถเชื่อม mysql ได้")
        aa=Entry(root,textvariable=sv1)           #creating entry box
        aa.grid(row=5,column=6)
        print "ไม่สามารถเชื่อม mysql ได้"
    except :
        print("Unknow error occured")
#    finally:
#        conn.close()
#        print('Connection closed.')


def printkri():
        c = canvas.Canvas("hello.pdf")
        c.setFont('THSarabunNew', 16)
        with open('./kriid.txt', 'r') as myfile:
            data=myfile.readline()
            list=data.split(",")
#            word=list[0]
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
        opener ="open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, "hello.pdf"])

def searchhn() :
    global aa7
    aaa = aa7.get()
    if aaa.isdigit():
        print "is number"
    else:
        print "is not number"
        sv1 = StringVar(root,value="HN ต้องใส่ตัวเลขเท่านั้น")
        aa=Entry(root,textvariable=sv1)           #creating entry box
        aa.grid(row=5,column=6)
        initkri()
        return
    khn2 = ""
    try:
        print('Connecting to MySQL database...')
        print db_config
        conn = MySQLConnection(**db_config)
#        conn = MySQLdb.connect (charset='utf8',host = "",user = "",passwd =,db = "")
        print('Connection Successful!!!')
        cursor = conn.cursor ()
        curex ="SELECT hn,name,surname,xn,brdate,id13 FROM krieng where trim(xn)<>'old' and hn="+aaa.strip()+";"
        cursor.execute (curex)
        acount = 0
        while True:
            rows = cursor.fetchmany ()
            if not rows:
                cursor.close ()
                conn.close ()
                if acount == 0:
                    print "ไม่พบid13 นี้"
                    sv1 = StringVar(root,value="ไม่พบid13 นี้")
                    aa=Entry(root,textvariable=sv1)           #creating entry box
                    aa.grid(row=5,column=6)
                    initkri()
                if acount >= 2:
                    print "มีid13 จำนวน"+str(acount)
                    sv1 = StringVar(root,value="มีid13 จำนวน"+str(acount))
                    aa=Entry(root,textvariable=sv1)           #creating entry box
                    aa.grid(row=5,column=6)
                break
            for row in rows:
                khn = row[0]
                khn2 = khn2+","+str(khn)
                print "HN =:", row[0]
                sv1 = StringVar(root,value=khn)
                aa=Entry(root,textvariable=sv1)           #creating entry box
                aa.grid(row=5,column=6)
#                Label(root,text=row[5]).grid(row=5,column=4) #Creating label
                Label(root,text="        "+row[5].strip()+"        ").grid(row=12,column=6) #Creating label
                print row[5]
                sv3 = StringVar(root,value=khn2)
                aa3=Entry(root,textvariable=sv3)           #creating entry box
                aa3.grid(row=6,column=6)
                sv4 = StringVar(root,value=row[1]+" "+row[2])
                aa4=Entry(root,textvariable=sv4)           #creating entry box
                aa4.grid(row=7,column=1)
                sv5 = StringVar(root,value='XN:'+row[3])
                aa5=Entry(root,textvariable=sv5)           #creating entry box
                aa5.grid(row=7,column=4)
                sv6 = StringVar(root,value=str(row[4]))
                aa6=Entry(root,textvariable=sv6)           #creating entry box
                aa6.grid(row=7,column=6)
                print khn
                print row[1]+" "+row[2]
                acount += 1
                print acount
#    except MySQLdb.Error as e:
    except Exception as e:
        print (e)
        sv1 = StringVar(root,value="ไม่สามารถเชื่อม mysql ได้")
        aa=Entry(root,textvariable=sv1)           #creating entry box
        aa.grid(row=5,column=6)
        print "ไม่สามารถเชื่อม mysql ได้"
    except :
        print("Unknow error occured")

def hex2bin2(hexval):
    print hexval
    r_data = binascii.unhexlify(hexval)
    stream = io.BytesIO(r_data)
    img = Image.open(stream)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf",14)
    draw.text((0, 220),"This is a test11",(0,255,0),font=font)
    draw = ImageDraw.Draw(img)
#    with open(img,'rb') as in_file: #error on here invalid file:
#        hex_data = in_file.read()
    # Unhexlify the data.
#    bin_data = binascii.unhexlify(bytes(hex_data))
    bin_data = binascii.unhexlify(bytes(hexval))
    print(bin_data)
    return
#    thelen = len(hexval)*4
#    binval = bin(int(hexval, 16))[2:]
#    krihex = int(str(hexval).strip(),16)
#    binval = bin(krihex)[2:]
#    while ((len(binval)) < thelen):
#        binval = '0' + binval
#    return binval


def hex2bin(self,str):
   bin = ['0000','0001','0010','0011',
         '0100','0101','0110','0111',
         '1000','1001','1010','1011',
         '1100','1101','1110','1111']
   aa = ''
#   abc = 'krieng'
   for i in range(len(str)):
       aa += bin[atoi(str[i],base=16)]
   return aa


def initkri():
    sv = StringVar(root,value='kriengsak')
    a=Entry(root,textvariable=sv)
    a.grid(row=5,column=1)
    Label(root,text="    id13 จากcard    ").grid(row=5,column=4) #Creating label
    Label(root,text="     id13 จากรพ    ").grid(row=12,column=6) #Creating label
#    sv2 = StringVar(root,value='ใส่ id13')
#    aa2=Entry(root,textvariable=sv2).grid(row=6,column=1)
    sv3 = StringVar(root,value='                   ')
    aa3=Entry(root,textvariable=sv3)
    aa3.grid(row=6,column=6)
    sv4 = StringVar(root,value='                   ')
    aa4=Entry(root,textvariable=sv4)
    aa4.grid(row=7,column=1)
    sv5 = StringVar(root,value='XN:  ')
    aa5=Entry(root,textvariable=sv5)
    aa5.grid(row=7,column=4)
    sv6 = StringVar(root,value='brith: ')
    aa6=Entry(root,textvariable=sv6)
    aa6.grid(row=7,column=6)

def imgkri(aaa):
#    c1=kriengten()
#    c1.openpicture('images.png')
    if aaa == '' :
        bbb ='images.jpg'
    else:
        bbb = aaa 
#    img =Image.open(bbb).convert('LA')
    img =Image.open(bbb)
    img.show()

def imgkri2():
#    bbb ='images.jpg'
#    img =Image.open(bbb)
#    img.show()
#    img.load()
#    img.thumbnail((250,250), Image.ANTIALIAS)
    c1=kriengten()
    c1.openpicture2('images.jpg')
    c1.kbarcode('123456')

#%reset -f
root=Tk()  #It is just a holder
root.title("Mpt Hospital")
root.resizable(width=True,height=True)
#root.geometry("300x300")
#root.configure(background='gray')

#panel = tk.Label(root, image = img)
#panel.pack(side = "bottom", fill = "both", expand = "yes")

sv = StringVar(root,value='kriengsak')
a=Entry(root,textvariable=sv)
a.grid(row=5,column=1)
sv1 = StringVar(root,value='HN')
aa=Entry(root,textvariable=sv1)
aa.grid(row=5,column=6)
sv2 = StringVar(root,value='ใส่ id13')
aa2=Entry(root,textvariable=sv2)
aa2.grid(row=6,column=1)
#sv7 = StringVar()
#sv7 = StringVar(root,value='ใส่ HN: ')
sv7 = StringVar(root,value='HN')
aa7=Entry(root,text="HN",textvariable=sv7)
aa7.grid(row=12,column=1)

initkri()

Label(root,text="ใส่ HN").grid(row=10,column=1) #Creating label
Label(root,text="id13 จาก รพ").grid(row=10,column=6) #Creating label
Label(root,text="ชื่อจาก card").grid(row=1,column=8) #Creating label
Label(root,text="วันเกิด จาก card").grid(row=5,column=8) #Creating label

Button(root,text="ใส่ idcard แล้วกดปุ่ม",command=readcard).grid(row=1,column=1)
Button(root,text="copy+id13จากCard",command=copyandfindid13).grid(row=1,column=4)
Button(root,text="พิมพ์ ใบสมัครงาน",command=printkri).grid(row=1,column=6)
Button(root,text="ค้น ID13",command=searchid13).grid(row=6,column=4)
Button(root,text="ค้น HN",command=searchhn).grid(row=12,column=4)
Button(root,text="แก้ไข id13 จากcardหลังค้นHN",command=copytocsv).grid(row=12,column=8)
Button(root,text="load photo+id13",command=photoid13).grid(row=15,column=1)
Button(root,text="open picture",command=imgkri2).grid(row=15,column=4)

root.mainloop() 