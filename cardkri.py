#! /usr/bin/env python
# -*- coding: utf-8 -*-
#this code is develop follow jane code for opensource user and programmer
# 2018-07-18 (Y-m-d)
# apt-get install pcscd python-pyscard
from reportlab.pdfgen import canvas
import subprocess, sys , os ,MySQLdb ,mysql.connector
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from tkFileDialog import askopenfilename
#from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_kri_config

pdfmetrics.registerFont(TTFont('THSarabunNew','THSarabunNew.ttf'))

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
    f1 = open('./kriid.txt','r')
    data=f1.readline()
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
#    tumbon = tumbon0[4:30]
    thaitumbon = unicode(tumbon0,"tis-620")
    tumbon1 = thaitumbon.replace(u'ตำบล',"")
    tumbon = tumbon1.encode('tis-620')
    amphur0 = words[6]
#    amphur = amphur0[5:30]
    thaiamphur = unicode(amphur0,"tis-620")
    amphur1 = thaiamphur.replace(u'อำเภอ',"")
    amphur = amphur1.encode('tis-620')
    province0 = words[7].strip()
#    province = province0[7:30]
    print province0
    print unicode(province0,"tis-620")
    thaiprovince = unicode(province0,"tis-620")
    province1 = thaiprovince.replace(u'จังหวัด',"")
    province = province1.encode('tis-620')
    f1.close
    csvfile = '../Dropbox/krifoxone/kriid.csv'
    if os.path.isfile(csvfile):
        f1 = open(csvfile,'w+')
        f1.write(id13+","+pre+name+" "+surname+","+birth+","+sex+","+address1+","+tumbon+","+amphur+","+province+","+name+","+surname+","+kripre)
        f1.close
        sv = StringVar(root,value='เริ่ม อ่านบัตร')
        print "start cardreader"
        a=Entry(root,textvariable=sv)           #creating entry box
        a.grid(row=5,column=1)
        sv2 = StringVar(root,value="HN")
        aa=Entry(root,textvariable=sv2)           #creating entry box
        aa.grid(row=5,column=6)
        print "HN"

#    print "เริ่ม open smartcard"
    else:
        print("ไม่พบ file kriid.csv")
        sv = StringVar(root,value='เปิด cardkri.py ผิดที่')
        print "start cardreader"
        a=Entry(root,textvariable=sv)           #creating entry box
        a.grid(row=5,column=1)
        sv2 = StringVar(root,value="HN")
        aa=Entry(root,textvariable=sv2)           #creating entry box
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
    time.sleep(100)

def xyz():
    global a
    aaa = aa2.get()
    print aaa 
    if len(aaa)<> 13:
                    print "ใส่เลขไม่ครบ 13 หลัก"
                    sv2 = StringVar(root,value="ใส่เลขไม่ครบ 13 หลัก")
                    aa=Entry(root,textvariable=sv2)           #creating entry box
                    aa.grid(row=5,column=6)
                    return
    
    db_config = read_kri_config()
    print db_config
    khn2 = ""
    try:
        print('Connecting to MySQL database...')
#        conn = MySQLConnection(**db_config)
        conn = MySQLdb.connect (host = "192.168.1.252",
                        user = "hospital",
                        passwd = db_config,
                        db = "tikisvn3")
        print('Connection Successful!!!')
        cursor = conn.cursor ()
        cursor.execute ("SELECT hn,name,surname FROM krieng where trim(xn)<>'old' and id13='"+aaa.strip()+"';")
        acount = 0
        while True:
#            row = cursor.fetchone ()
            rows = cursor.fetchmany ()
            if not rows:
                if acount == 0:
                    print "ไม่พบid13 นี้"
                    sv2 = StringVar(root,value="ไม่พบid13 นี้")
                    aa=Entry(root,textvariable=sv2)           #creating entry box
                    aa.grid(row=5,column=6)
                if acount >= 2:
                    print "มีid13 จำนวน"+str(acount)
                    sv2 = StringVar(root,value="มีid13 จำนวน"+str(acount))
                    aa=Entry(root,textvariable=sv2)           #creating entry box
                    aa.grid(row=5,column=6)
                break
            for row in rows:
#            if row is None :   # row ==None
                if row == None and acount==0:   # row ==None
                    print "ไม่พบid13 นี้"
                    sv2 = StringVar(root,value="aaa ไม่พบid13 นี้")
                    aa=Entry(root,textvariable=sv2)           #creating entry box
                    aa.grid(row=5,column=6)
                    break
                if row == None and acount>0:   # row ==None
                    print "มีid13 จำนวน"+str(acount)
                    sv2 = StringVar(root,value="มีid13 จำนวน"+str(acount))
                    aa=Entry(root,textvariable=sv2)           #creating entry box
                    aa.grid(row=5,column=6)
                    break
                
                khn = row[0]
                khn2 = khn2+","+str(khn)
                print "HN =:", row[0]
#                cursor.close ()
#                conn.close ()
                sv2 = StringVar(root,value=khn)
                aa=Entry(root,textvariable=sv2)           #creating entry box
                aa.grid(row=5,column=6)
                sv4 = StringVar(root,value=khn2)
                aa3=Entry(root,textvariable=sv4)           #creating entry box
                aa3.grid(row=6,column=6)
# 
#               
#  print khn+" "+row[1]+" "+row[2]
                print khn
                print u"row[1]"
                acount += 1
                print acount

    except MySQLdb.Error as e:
        print (e)
        sv2 = StringVar(root,value="ไม่สามารถเชื่อม mysql ได้")
        aa=Entry(root,textvariable=sv2)           #creating entry box
        aa.grid(row=5,column=6)
        print "ไม่สามารถเชื่อม mysql ได้"
    except :
        print("Unknow error occured")

def findhn():
    db_config = read_kri_config()
    print db_config
    try:
        print('Connecting to MySQL database...')
#        conn = MySQLConnection(**db_config)
        conn = MySQLdb.connect (host = "192.168.1.252",
                        user = "hospital",
                        passwd = db_config,
                        db = "tikisvn3")
#        if conn.is_connected():
        print('Connection Successful!!!')
        cursor = conn.cursor ()
        myfile = open('./kriid.txt','r')
        data=myfile.readline()
        list=data.split(",")
        kid13=list[0]
        print kid13
        cursor.execute ("SELECT hn,name,surname FROM krieng where id13='"+kid13+"';")
#        row = cursor.fetchone ()
        acount = 0
        while True:
            row = cursor.fetchone ()
#            if row is None :   # row ==None
            if row == None and acount==0:   # row ==None
                print "ไม่พบid13 นี้"
                sv2 = StringVar(root,value="ไม่พบid13 นี้")
                aa=Entry(root,textvariable=sv2)           #creating entry box
                aa.grid(row=5,column=6)
                break
            if row is None and acount>0:   # row ==None
                print "มีid13 จำนวน"+str(acount)
                sv2 = StringVar(root,value="มีid13 จำนวน"+str(acount))
                aa=Entry(root,textvariable=sv2)           #creating entry box
                aa.grid(row=5,column=6)
                break
            
            khn = row[0]
            print "HN =:", row[0]
            cursor.close ()
            conn.close ()
            sv2 = StringVar(root,value=khn)
            aa=Entry(root,textvariable=sv2)           #creating entry box
            aa.grid(row=5,column=6)
            print khn+" "+row[1]+" "+row[2]
            acount += 1
    except MySQLdb.Error as e:
        print (e)
        sv2 = StringVar(root,value="ไม่สามารถเชื่อม mysql ได้")
        aa=Entry(root,textvariable=sv2)           #creating entry box
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
        opener ="open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, "hello.pdf"])


from Tkinter import *
#from Tkinter import Tk, Button, Frame, Entry,Label, END
from smartcard.System import readers
import binascii

root=Tk()  #It is just a holder

Label(root,text="test enter").grid(row=10,column=1) #Creating label
sv = StringVar(root,value='kriengsak')
sv2 = StringVar(root,value='HN')
sv3 = StringVar(root,value='ใส่ id13')
sv4 = StringVar(root,value='                   ')
a=Entry(root,textvariable=sv)           #creating entry box
a.grid(row=5,column=1)
aa=Entry(root,textvariable=sv2)           #creating entry box
aa.grid(row=5,column=6)
aa2=Entry(root,textvariable=sv3)           #creating entry box
aa2.grid(row=6,column=1)
aa3=Entry(root,textvariable=sv4)           #creating entry box
aa3.grid(row=6,column=6)

Button(root,text="OK",command=xyz).grid(row=10,column=8)
Button(root,text="ค้น HN",command=findhn).grid(row=1,column=8)
Button(root,text="ใส่ idcard แล้วกดปุ่ม",command=readcard).grid(row=1,column=1)
Button(root,text="copy ข้อมูล",command=copytocsv).grid(row=1,column=4)
Button(root,text="พิมพ์ ใบสมัครงาน",command=printkri).grid(row=1,column=6)

root.mainloop() 