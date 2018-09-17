#! /usr/bin/env python
# -*- coding: utf-8 -*

#from __future__ import print_function
import future        # pip install future
import builtins      # pip install future
import past          # pip install future
import six           # pip install six
from builtins import bytes
from six.moves import tkinter as tk
from six.moves import tkinter_messagebox as messagebox
import tkinter.scrolledtext as tkscrolled
import tkinter as tk
from tkinter import StringVar,Entry,Label,Button , ttk ,Frame ,Text,Listbox
#from Tkinter import *
#from ttk import *
import socket
import _thread
from netifaces import interfaces, ifaddresses, AF_INET

class ChatClient(Frame):
  
  def __init__(self, root):
    Frame.__init__(self, root)
    self.root = root
    self.initUI()
    self.serverSoc = None
    self.serverStatus = 0
    self.buffsize = 1024
    self.allClients = {}
    self.counter = 0
    self.handleSetServer()
    if self.localip =='192.168.1.152' or self.localip == '192.168.2.106' :
      print ("pass")
      pass
    else:
      self.handleAddClient() 

  def initUI(self):
    self.root.title("Simple P2P Chat Client")
    ScreenSizeX = self.root.winfo_screenwidth()
    ScreenSizeY = self.root.winfo_screenheight()
    print (ScreenSizeX)
    print (ScreenSizeY)
#    ccc = 0
    for ifaceName in interfaces():
        abc = ''
        addresses = [i['addr']
        for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr':'No IP addr'}] )]
        abc = ''.join(addresses)
        print abc[0:3]
        if abc[0:3] == '192':
          self.localip = ''.join(addresses)
          print (str(self.localip))
        print '%s: %s' % (ifaceName, ', '.join(addresses))
#        ccc = ccc+1


    self.FrameSizeX  = 800
    self.FrameSizeY  = 600
#    FramePosX   = (ScreenSizeX - self.FrameSizeX)/2
#    FramePosY   = (ScreenSizeY - self.FrameSizeY)/2
#    self.FrameSizeX  = 800
#    self.FrameSizeY  = 600
    FramePosX   = 100
    FramePosY   = 100
    self.root.geometry("%sx%s+%s+%s" % (self.FrameSizeX,self.FrameSizeY,FramePosX,FramePosY))
#    self.root.resizable(width=False, height=False)
    self.root.resizable(width=True, height=True)
    
    padX = 10
    padY = 10
    parentFrame = Frame(self.root)
#    parentFrame.grid(padx=padX, pady=padY, stick=E+W+N+S)
    parentFrame.grid(padx=padX, pady=padY, stick=tk.E+tk.W+tk.N+tk.S)
    
    ipGroup = Frame(parentFrame)
    serverLabel = Label(ipGroup, text="Set: ")
    self.nameVar = StringVar()
    self.nameVar.set("SDH")
    nameField = Entry(ipGroup, width=10, textvariable=self.nameVar)
    self.serverIPVar = StringVar()
#    self.serverIPVar.set("127.0.0.1")
    self.serverIPVar.set(self.localip)
    serverIPField = Entry(ipGroup, width=15, textvariable=self.serverIPVar)
    self.serverPortVar = StringVar()
    self.serverPortVar.set("8090")
    serverPortField = Entry(ipGroup, width=5, textvariable=self.serverPortVar)
    serverSetButton = Button(ipGroup, text="Set", width=10, command=self.handleSetServer)
    addClientLabel = Label(ipGroup, text="Add friend: ")
    self.clientIPVar = StringVar()
#    self.clientIPVar.set("192.168.1.152")
    self.clientIPVar.set("192.168.2.106")
    clientIPField = Entry(ipGroup, width=15, textvariable=self.clientIPVar)
    self.clientPortVar = StringVar()
    self.clientPortVar.set("8090")
    clientPortField = Entry(ipGroup, width=5, textvariable=self.clientPortVar)
    clientSetButton = Button(ipGroup, text="Add", width=10, command=self.handleAddClient)
    serverLabel.grid(row=0, column=0)
    nameField.grid(row=0, column=1)
    serverIPField.grid(row=0, column=2)
    serverPortField.grid(row=0, column=3)
    serverSetButton.grid(row=0, column=4, padx=5)
    addClientLabel.grid(row=0, column=5)
    clientIPField.grid(row=0, column=6)
    clientPortField.grid(row=0, column=7)
    clientSetButton.grid(row=0, column=8, padx=5)
    
    readChatGroup = Frame(parentFrame)
    self.receivedChats = Text(readChatGroup, bg="white", width=60, height=20, state=tk.DISABLED)
#    self.receivedChats = Text(readChatGroup, bg="white", width=60, height=20)
    self.receivedChats.config(font=("consolas",12),undo=True,wrap='word')
#    self.vsb = tk.Scrollbar(self,orient="vertical",command=self.receivedChats.yview)
#    self.receivedChats.configure(yscrollcommand=self.vsb.set)
#    self.vsb.pack(side="right",fill="y")
#    self.receivedChats.pack(side="left",fill="both",expand=True)

#    self.receivedChats.config(font=("tahoma",12),undo=True,wrap='word')
#    self.TKScrollTXT = tkscrolled.ScrolledText(10, width=60, height=20, wrap='word')
#    self.receivedChats = TKScrollTXT
#    self.receivedChats = Text(readChatGroup, bg="white", width=60, height=20, state=tk.DISABLED)
    self.friends = Listbox(readChatGroup, bg="white", width=30, height=20)
    self.receivedChats.grid(row=0, column=0, sticky=tk.W+tk.N+tk.S, padx = (0,10))
    self.friends.grid(row=0, column=1, sticky=tk.E+tk.N+tk.S)

    # create a Scrollbar and associate it with txt
#    scrollb = tki.Scrollbar(txt_frm, command=self.txt.yview)
#    scrollb.grid(row=0, column=1, sticky='nsew')
#    self.txt['yscrollcommand'] = scrollb.set



    writeChatGroup = Frame(parentFrame)
    self.chatVar = StringVar()
    self.chatField = Entry(writeChatGroup, width=80, textvariable=self.chatVar)
    sendChatButton = Button(writeChatGroup, text="Send", width=10, command=self.handleSendChat)
    self.chatField.grid(row=0, column=0, sticky=tk.W)
    sendChatButton.grid(row=0, column=1, padx=5)

    self.statusLabel = Label(parentFrame)

#    bottomLabel = Label(parentFrame, text="Created by Siddhartha Sahu (sh.siddhartha@gmail.com) under Prof. A. Prakash [Computer Networks, Dept. of CSE, BIT Mesra]")
    ktext = 'โรงพยาบาลเมืองปทุม 24/3 ถ.ปทุมสัมพันธ์ อ.เมือง จ.ปทุมธานี โทร 025816226'
    bottomLabel = Label(parentFrame, text=ktext)
    
    ipGroup.grid(row=0, column=0)
    readChatGroup.grid(row=1, column=0)
    writeChatGroup.grid(row=2, column=0, pady=10)
    self.statusLabel.grid(row=3, column=0)
    bottomLabel.grid(row=4, column=0, pady=10)
#    self.serverSoc = None
#    self.handleSetServer()


  def handleSetServer(self):
    if self.serverSoc != None:
        self.serverSoc.close()
        self.serverSoc = None
        self.serverStatus = 0
    serveraddr = (self.serverIPVar.get().replace(' ',''), int(self.serverPortVar.get().replace(' ','')))
    try:
        self.serverSoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSoc.bind(serveraddr)
        self.serverSoc.listen(5)
        self.setStatus("Server listening on %s:%s" % serveraddr)
        _thread.start_new_thread(self.listenClients,())
        self.serverStatus = 1
        self.name = self.nameVar.get().replace(' ','')
        if self.name == '':
            self.name = "%s:%s" % serveraddr
    except:
        self.setStatus("Error setting up server")
    
  def listenClients(self):
    while 1:
      clientsoc, clientaddr = self.serverSoc.accept()
      self.setStatus("Client connected from %s:%s" % clientaddr)
      self.addClient(clientsoc, clientaddr)
      _thread.start_new_thread(self.handleClientMessages, (clientsoc, clientaddr))
    self.serverSoc.close()
  
  def handleAddClient(self):
    if self.serverStatus == 0:
      self.setStatus("Set server address first")
      return
    clientaddr = (self.clientIPVar.get().replace(' ',''), int(self.clientPortVar.get().replace(' ','')))
    try:
        clientsoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientsoc.connect(clientaddr)
        self.setStatus("Connected to client on %s:%s" % clientaddr)
        self.addClient(clientsoc, clientaddr)
        _thread.start_new_thread(self.handleClientMessages, (clientsoc, clientaddr))
    except:
        self.setStatus("Error connecting to client")

  def handleClientMessages(self, clientsoc, clientaddr):
    while 1:
      try:
        data = clientsoc.recv(self.buffsize)
        if not data:
            break
        self.addChat("%s:%s" % clientaddr, data)
      except:
          break
    self.removeClient(clientsoc, clientaddr)
    clientsoc.close()
    self.setStatus("Client disconnected from %s:%s" % clientaddr)
  
  def handleSendChat(self):
    if self.serverStatus == 0:
      self.setStatus("Set server address first")
      return
    msg = self.chatVar.get().replace(' ','')
    if msg == '':
        return
    self.addChat("me", msg)
    for client in self.allClients.keys():
      client.send(msg)
  
  def addChat(self, client, msg):
    self.receivedChats.config(state=tk.NORMAL)
    self.receivedChats.insert("end",client+": "+msg+"\n")
    self.receivedChats.see("end")
    self.receivedChats.config(state=tk.DISABLED)
  
  def addClient(self, clientsoc, clientaddr):
    self.allClients[clientsoc]=self.counter
    self.counter += 1
    self.friends.insert(self.counter,"%s:%s" % clientaddr)
  
  def removeClient(self, clientsoc, clientaddr):
      print (self.allClients)
      self.friends.delete(self.allClients[clientsoc])
      del self.allClients[clientsoc]
      print (self.allClients)
  
  def setStatus(self, msg):
    self.statusLabel.config(text=msg)
    print (msg)
      
def main():  
  root = tk.Tk()
  app = ChatClient(root)
#  app.pack(fill="both",expand=True)
  root.mainloop()  

if __name__ == '__main__':
  main()  