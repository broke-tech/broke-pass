from PyQt5.QtCore import Qt,QTimer
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,QSpacerItem, QLabel, QLineEdit, QComboBox,
    QPushButton, QFileDialog, QScrollArea,QDialog,QSizePolicy,
    QGroupBox, QFormLayout, QMessageBox,QFrame)
from PyQt5.QtGui import QColor,QPalette,QPixmap,QFontDatabase,QFont,QIcon
import sys
import os
import json
from webbrowser import open as opensite
from shutil import move as movefile
import random
import string
import requests
from pyperclip import copy as copytext
from datetime import datetime
import subprocess

dir = os.getcwd()
developer = "@br0ke.tech"
version = "1.1 ALPHA"
newstuff = ["fonts"]

try:
    releasenotesurl = "https://raw.githubusercontent.com/broke-tech/broke-pass/refs/heads/main/releasenotes"
    r = requests.get(releasenotesurl)
    with open(os.path.join(dir, "assets", "updates.json"), "w") as cfg_file:
        cfg_file.write(r.text)
except:
    pass

if not os.path.exists(os.path.join(dir, "assets", "updates.json")):
    with open(os.path.join(dir, "assets", "updates.json"), "w") as file:
        json.dump({"latest":version,"releases":{version:{"name":"1.0","notes":"None"}}},file)

with open(os.path.join(dir,"assets","updates.json"),encoding="utf-8") as file:
    updatenotes = json.load(file)

versionup = updatenotes["latest"]
curenc = 2
if version == versionup:
    updateavailable = False
else:
    updateavailable = True

availablenotes = updatenotes["releases"][versionup]["notes"]

class Pwd():
    def __init__(self,uix,name,pwd,fav):
        self.name = name
        self.pwd = pwd
        self.uix = uix
        self.fav = fav

        self.counter = -1
        counter = -1
        for i in self.uix.enc.decrpasswords:
            counter += 1
            if i.split(" ")[0] == self.name:
                self.counter = counter
                break

        self.l = QVBoxLayout()
        uix.passl.addLayout(self.l)
        self.lh = QHBoxLayout()
        self.l.addLayout(self.lh)
        
        self.lh2 = QHBoxLayout()
        self.l.addLayout(self.lh2)
        
        self.passline = QLineEdit(pwd)
        self.passline.setReadOnly(True)
        self.passbutton = QPushButton(self.uix.lang["generate"][self.uix.curlang])
        self.passbutton.clicked.connect(lambda:self.generate())
        self.editbutton = QPushButton(self.uix.lang["edit"][self.uix.curlang])
        self.editbutton.clicked.connect(lambda:self.openedit())
        self.hidebutton = QPushButton(self.uix.lang["hide"][self.uix.curlang])
        self.hidebutton.clicked.connect(lambda:self.hidepass())
        self.copybutton = QPushButton(self.uix.lang["copy"][self.uix.curlang])
        self.copybutton.clicked.connect(lambda:copytext(str(self.pwd)))
        self.lname = QLabel(f"{self.checkfav()}{self.name}")
        self.lh.addWidget(self.lname)
        self.lh.addWidget(self.editbutton)
        self.lh.addStretch()
        self.lh2.addWidget(self.passline)
        self.lh2.addWidget(self.hidebutton)
        self.lh2.addWidget(self.copybutton)
        self.l.addWidget(QLabel(""))

        self.editdialogbox = QDialog()
        self.editlayout = QVBoxLayout()
        self.editdialogbox.setWindowIcon(QIcon(uix.logo))
        self.editdialogbox.setLayout(self.editlayout)
        self.editname = QLabel(f"{self.checkfav()}{self.name} - {self.uix.lang["edit"][self.uix.curlang]}")
        self.editwebsite = QLineEdit()
        self.editpassword = QLineEdit()
        self.editsave = QPushButton(self.uix.lang["save"][self.uix.curlang])
        self.editsave.clicked.connect(self.saveedit)
        self.editdel = QPushButton(self.uix.lang["delete"][self.uix.curlang])
        self.editdel.clicked.connect(self.delete)
        self.editfav = QPushButton(self.uix.lang["addfavs"][self.uix.curlang])
        self.editfav.clicked.connect(self.setfav)
        self.editcancel = QPushButton(self.uix.lang["cancel"][self.uix.curlang])
        self.editcancel.clicked.connect(lambda:self.editdialogbox.hide())
        self.edittitlel = QHBoxLayout()
        self.edittitlel.addWidget(self.editname)
        self.edittitlel.addStretch()
        self.edittitlel.addWidget(self.editfav)
        self.edittitlel.addWidget(self.editdel)
        self.editlayout.addLayout(self.edittitlel)
        self.editlayout.addWidget(self.editwebsite)
        self.edith1 = QHBoxLayout()
        self.edith1.addWidget(self.editpassword)
        self.edith1.addWidget(self.passbutton)
        self.edith2 = QHBoxLayout()
        self.edith2.addWidget(self.editcancel)
        self.edith2.addWidget(self.editsave)
        self.editlayout.addLayout(self.edith1)
        self.editlayout.addLayout(self.edith2)
        self.hidestate = False
        if self.uix.config["hide"] == "1":
            self.hidepass()
        self.replace()

    def openedit(self):
        self.replace()
        self.editdialogbox.show()

    def checkfav(self):
        if self.fav == "f":
            return "⭐"
        else:
            return ""
    
    def checkfavbut(self):
        if self.fav == "f":
            return self.uix.lang["removefavs"][self.uix.curlang]
        else:
            return self.uix.lang["addfavs"][self.uix.curlang]

    def setfav(self):
        if self.fav == "f":
            self.fav = "n"
        else:
            self.fav = "f"
        self.editdialogbox.hide()
        self.saveedit()

    def saveedit(self):
        if len(self.editwebsite.text()) != 0 and len(self.editpassword.text()) != 0:
            for i in self.uix.enc.decrpasswords:
                if i.split(" ")[0] == self.editwebsite.text() and i.split(" ")[0] != self.name:
                    self.uix.messagebox(self.uix.lang["alreadyentry"][self.uix.curlang])
                    return False
            if " " in self.editwebsite.text() or " " in self.editpassword.text():
                self.uix.messagebox(self.uix.lang["yetanotherspace"][self.uix.curlang])
                return False
        else:
            self.uix.messagebox(self.uix.lang["masterspaces"][self.uix.curlang])
            return False
        self.pwd = self.editpassword.text()
        self.name = self.editwebsite.text()
        self.replace()     
        self.savepass()
        self.uix.addpasswords()
        self.editdialogbox.hide()

    def delete(self):
        self.uix.dialog(ui.lang["sure"][ui.curlang],self.uix.lang["deletewarn"][self.uix.curlang],ui.lang["yes"][ui.curlang],ui.lang["no"][ui.curlang])
        if self.uix.yesno:
            del self.uix.enc.decrpasswords[self.counter]
            self.uix.addpasswords()
            self.uix.enc.encryptsave()
            self.editdialogbox.hide()
        
    def generate(self):
        length = 12
        random_string = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=length))
        self.editpassword.setText(random_string)

    def hidepass(self):
        if self.hidestate == False:
            self.pwd = self.passline.text()
            self.passline.setText(self.pwd)
            self.passline.setEchoMode(QLineEdit.PasswordEchoOnEdit)
            self.hidestate = True
            self.hidebutton.setText(self.uix.lang["show"][self.uix.curlang])
        else:
            self.pwd = self.passline.text()
            self.passline.setText(self.pwd)
            self.passline.setEchoMode(QLineEdit.Normal)
            self.hidestate = False
            self.hidebutton.setText(self.uix.lang["hide"][self.uix.curlang])

    def replace(self):
        self.editname.setText(f"{self.checkfav()}{self.name} - {self.uix.lang["edit"][self.uix.curlang]}")
        self.editpassword.setText(self.pwd)
        self.editwebsite.setText(self.name)
        self.editfav.setText(self.checkfavbut())
        self.passline.setText(self.pwd)
        self.lname.setText(f"{self.checkfav()}{self.name}") 

    def savepass(self):
        self.uix.enc.decrpasswords[self.counter] = f"{self.name} {self.pwd} {self.fav}"
        self.uix.enc.encryptsave()

class SettingCombo():
    def __init__(self,textl=str,textwarn=str,layout=QHBoxLayout or QVBoxLayout,config=str,items=list,uix=None):
        self.l = QHBoxLayout()
        self.uix = uix
        self.configtext = config
        layout.addLayout(self.l)
        self.combo = QComboBox()
        self.combo.addItems(items)
        self.combo.setCurrentIndex(self.gettext())
        self.combo.currentTextChanged.connect(self.change)
        self.l.addWidget(QLabel(textl))
        self.l.addWidget(self.combo)

        self.filel = QHBoxLayout()
        self.fileg = QGroupBox()
        self.fileg.hide()
        self.fileg.setLayout(self.filel)
        layout.addWidget(self.fileg)
        self.fileline = QLineEdit()
        self.fileline.setReadOnly(True)
        self.filebut = QPushButton(self.uix.lang["change"][self.uix.curlang])
        self.filebut.clicked.connect(self.changefile)
        self.filel.addWidget(QLabel(f"{self.uix.lang["current"][self.uix.curlang]}"))
        self.filel.addWidget(self.fileline)
        self.filel.addWidget(self.filebut)
        if self.configtext == "file":
            self.fileg.hide()
            if self.uix.config["file"] == "0":
                self.fileline.setText(str(self.uix.config["filelocation"]))
                self.fileg.show()
            elif self.uix.config["file"] == "1":
                self.fileline.setText("//Choose each time//")
                self.fileg.hide()

        self.desc = QLabel(f"{textwarn}\n")
        self.uix.setsize(self.desc,15)
        self.desc.setWordWrap(True)
        layout.addWidget(self.desc)
    
    def gettext(self):
        try:
            return int(self.uix.config[self.configtext])
        except:
            return int("0")

    def change(self):
        if self.configtext != "file":
            self.uix.config[self.configtext] = str(self.combo.currentIndex())
            with open(os.path.join(dir,"assets","config.json"),"w",encoding="utf-8") as file:
                json.dump(self.uix.config,file)
            self.uix.appstyle()
        else:
            if self.combo.currentIndex() == 0:
                self.uix.config[self.configtext] = str(self.combo.currentIndex())
                filework = QFileDialog.getOpenFileName(ui,"Select your passwords file","","Broke Pass file (*.bpass)")
                if filework[0] != "":
                    self.uix.config["filelocation"] = filework[0]
                    with open(os.path.join(dir,"assets","config.json"),"w",encoding="utf-8") as file:
                        json.dump(self.uix.config,file)
                    self.fileline.setText(filework[0])
                    self.fileg.show()
                else:
                    self.uix.config[self.configtext] = str(self.combo.currentIndex())
                    self.combo.setCurrentIndex(1)
                    self.fileg.hide()
            elif self.combo.currentIndex() == 1:
                self.uix.config[self.configtext] = str(self.combo.currentIndex())
                self.uix.config["filelocation"] = self.uix.filelocation
                with open(os.path.join(dir,"assets","config.json"),"w",encoding="utf-8") as file:
                    json.dump(self.uix.config,file)
                self.fileline.setText(self.uix.filelocation)
                self.fileg.hide()
            else:
                self.uix.config[self.configtext] = str(self.combo.currentIndex())
                self.fileline.setText("//Choose each time//")
                self.fileg.hide()
            self.uix.config[self.configtext] = str(self.combo.currentIndex())
            with open(os.path.join(dir,"assets","config.json"),"w",encoding="utf-8") as file:
                json.dump(self.uix.config,file)
            self.uix.appstyle()

    def changefile(self):
        if self.combo.currentIndex() == 0:
            filework = QFileDialog.getOpenFileName(ui,"Select your passwords file","","Broke Pass file (*.bpass)")
            if filework[0] != "":
                self.uix.config["filelocation"] = filework[0]
                with open(os.path.join(dir,"assets","config.json"),"w",encoding="utf-8") as file:
                    json.dump(self.uix.config,file)
                self.fileline.setText(filework[0])
                self.fileg.show()

class Encryption():
    def __init__(self,uix):
        self.encryptkeys2 = #ENCRYPTION
        self.decryptkeys2 = {v: k for k, v in self.encryptkeys2.items()}
        print(self.encrypttext("brokeuser default\nbrokepassword default",self.encryptkeys2))
        self.uix = uix

    def encrypttext(self,text,encryption):
        encrlist = []
        for i in text:
            try:
                encrlist.append(encryption[i])
            except:
                encrlist.append(i) #NOT ENCRYPTABLE
        final = ''.join(encrlist)
        return(final)
    
    def decrypttext(self,text,decryption):
        decrlist = []
        for i in text:
            try:
                decrlist.append(decryption[i])
            except:
                decrlist.append(i) #NOT DECRYPTABLE
            
        final = ''.join(decrlist)
        return(final)

    def foolproof(self,filecur):
        if os.path.exists(os.path.join(filecur)):
            with open(os.path.join(filecur),"r",encoding="utf-8") as file:
                encrpasswords = file.read().splitlines()
            decrpasswords = []
            m = False
            u = False
            v = False
            version = -1
            for i in encrpasswords:
                if self.decrypttext(i,self.decryptkeys2).split(" ")[0] != "brokepassword" and self.decrypttext(i,self.decryptkeys2).split(" ")[0] != "brokeuser" and self.decrypttext(i,self.decryptkeys2).split(" ")[0] != "version":
                    decrpasswords.append(self.decrypttext(i,self.decryptkeys2))
                elif self.decrypttext(i,self.decryptkeys2).split(" ")[0] == "brokepassword":
                    masterpassword = self.decrypttext(i,self.decryptkeys2).split(" ")[1]
                    m = True
                elif self.decrypttext(i,self.decryptkeys2).split(" ")[0] == "brokeuser":
                    user = self.decrypttext(i,self.decryptkeys2).split(" ")[1]
                    u = True
            if m == False:
                self.uix.messagebox(self.uix.lang["corrupt"][self.uix.curlang])
                self.changeuser(os.path.join(dir,"assets","default.bpass"),self.uix)
                return False
            if u == False:
                self.uix.messagebox(self.uix.lang["corrupt"][self.uix.curlang])
                self.changeuser(os.path.join(dir,"assets","default.bpass"),self.uix)
                return False
            return True
        else:
            return False

    def properjson(self,jsonf):
        l = []
        for i in str(jsonf):
            if i == "'":
                l.append('"')
            else:
                l.append(i)
        return ''.join(l)

    def decryptopen(self,filecur):
        if self.foolproof(filecur) == True:
            with open(os.path.join(filecur),encoding="utf-8") as file:
                self.encrpasswords = file.read().splitlines()
            self.decrpasswords = []
            self.uix.filelocation = filecur
            for i in self.encrpasswords:
                if self.decrypttext(i,self.decryptkeys2).split(" ")[0] != "brokepassword" and self.decrypttext(i,self.decryptkeys2).split(" ")[0] != "brokeuser":
                    self.decrpasswords.append(self.decrypttext(i,self.decryptkeys2))
                elif self.decrypttext(i,self.decryptkeys2).split(" ")[0] == "brokepassword":
                    self.masterpassword = self.decrypttext(i,self.decryptkeys2).split(" ")[1]
                elif self.decrypttext(i,self.decryptkeys2).split(" ")[0] == "brokeuser":
                    self.user = self.decrypttext(i,self.decryptkeys2).split(" ")[1]

    def encryptsave(self):
        mastersave = self.encrypttext(f"brokepassword {self.masterpassword}\n",self.encryptkeys2)
        usersave = self.encrypttext(f"brokeuser {self.user}\n",self.encryptkeys2)
        self.encrpasswords = self.encrypttext("\n".join(self.decrpasswords),self.encryptkeys2)
        with open(os.path.join(self.uix.filelocation),"w",encoding="utf-8") as file:
            file.write(mastersave+usersave+self.encrpasswords)

    def export(self):
        ui.dialog(ui.lang["sure"][ui.curlang],ui.lang["exportmsg"][ui.curlang],ui.lang["yes"][ui.curlang],ui.lang["no"][ui.curlang])
        if ui.yesno:
            self.exportpasswords = "\n".join(self.decrpasswords)
            mastersave = f"brokepassword {self.masterpassword}\nbrokeuser {self.user}\n"
            with open(os.path.join(dir,"assets","export.txt"),"w",encoding="utf-8") as file:
                file.write(mastersave+self.exportpasswords+f"\n"+self.properjson(str(self.uix.config)))
            date = datetime.now()
            fname = f"{date.strftime("%m")}-{date.strftime("%d")}-{date.strftime("%y")}export.brokepass"
            movefile(os.path.join(dir,"assets","export.txt"),os.path.join(dir,"assets","exports",fname))
            ui.messagebox(f"Exported successfully at {os.path.join(dir,"assets","exports",fname)}")

    def importpass(self):
        ui.dialog(ui.lang["sure"][ui.curlang],ui.lang["importmsg"][ui.curlang],ui.lang["yes"][ui.curlang],ui.lang["no"][ui.curlang])
        if ui.yesno:    
            filework = QFileDialog.getOpenFileName(ui,"Select a brokepass file","","Broke Pass export (*.brokepass)")
            if filework[0] != "":
                with open(filework[0],"r",encoding="utf-8") as file:
                    imported = file.read()
                passwords = self.encrypttext("\n".join(imported.split("\n")[0:len(imported.split("\n"))-1]),self.encryptkeys2)
                with open(os.path.join(self.uix.filelocation),"w",encoding="utf-8") as file:
                    file.write(passwords)

                tojson = json.loads(self.properjson(imported.split("\n")[-1]))
                tojson["filelocation"] = self.uix.filelocation
                with open(os.path.join(dir,"assets","config.json"),"w",encoding="utf-8") as file:
                    json.dump(tojson, file)
                ui.messagebox(ui.lang["restartapply"][ui.curlang])
                sys.exit()
    
    def createnewuser(self):
        if self.uix.newusername.text() != '' and self.uix.newuserpasswordline.text() != "":
            if " " not in self.uix.newusername.text() and " " not in self.uix.newuserpasswordline.text():
                if self.uix.newusername.text() != "default":
                    location = QFileDialog.getSaveFileName(self.uix,"Create new password file","","Broke Pass (*.bpass)","Broke Pass (*.bpass)")[0]
                    if location != "":
                        with open(os.path.join(location),"w",encoding="utf-8") as file:
                            file.write(self.encrypttext(f"brokepassword {self.uix.newuserpasswordline.text()}\nbrokeuser {self.uix.newusername.text()}",self.encryptkeys2))
                    self.changeuser(location,self.uix)
                    self.uix.newuserdialogbox.hide()
                else:
                    self.uix.messagebox(self.uix.lang["cantdefault"][self.uix.curlang])
            else:
                self.uix.messagebox(self.uix.lang["anothernospace"][self.uix.curlang])
                return False
        else:
            self.uix.messagebox(self.uix.lang["fillall"][self.uix.curlang])
            return False

    def changeuser(self,location,uix):
        if location != "":
            self.decryptopen(location)
            self.uix.loginline.clear()
            uix.logindmessage.setText(f"{self.uix.lang["entermaster"][self.uix.curlang]}\n@{self.user}")
            if len(location) > 70:
                uix.loginlocation.setText(f"{self.uix.lang["current"][self.uix.curlang]}{location[0:70]}...")
            else:
                uix.loginlocation.setText(f"{self.uix.lang["current"][self.uix.curlang]}{location}")
            if len(location) > 70:
                uix.settingslocation.setText(f"{self.uix.lang["current"][self.uix.curlang]}{location[0:70]}...")
            else:
                uix.settingslocation.setText(f"{self.uix.lang["current"][self.uix.curlang]}{location}")
            uix.passwordmaster.setText(self.masterpassword)
            uix.username.setText(self.user)
            uix.loginduserg.hide()
            uix.logindnouserg.hide()
            if self.user == "default":
                uix.loginduserg.hide()
                uix.logindnouserg.show()
            elif self.user != "default":
                uix.loginduserg.show()
                uix.logindnouserg.hide()

class Button():
    def __init__(self,name,id,uix):
        self.button = QPushButton(name)
        self.id = id
        self.button.clicked.connect(lambda:self.change())
        self.uix = uix
        self.uix.sidel.addWidget(self.button,alignment=Qt.AlignLeft)

    def change(self):
        if self.id != "l":
            for i in [self.uix.maing,self.uix.setg,self.uix.homeg,self.uix.aboutg,self.uix.updatesg]:
                i.hide()
            for i in self.uix.sectionbuts:
                if self.uix.config["mode"] == "0": style = self.uix.styles["nobgblack"] 
                else: style = self.uix.styles["nobgwhite"]
                i.button.setStyleSheet(style)
                i.button.setIcon(QIcon(os.path.join(dir,"assets","icons",f"{i.id}{self.uix.config["mode"]}")))
            self.button.setStyleSheet(self.uix.styles["selbut"])
            self.button.setIcon(QIcon(os.path.join(dir,"assets","icons",f"{self.id}0")))
            if self.id == "s":
                self.uix.setg.show()
            if self.id == "h":
                self.uix.homeg.show()
            if self.id == "p":
                self.uix.maing.show()
            if self.id == "a":
                self.uix.aboutg.show()
            if self.id == "u":
                self.uix.updatesg.show()
        else:
            self.uix.dialog("Are you sure?","Your unsaved work will be lost! You will also need to enter your master password again in order to log back in! Continue?","Yes","No")
            if self.uix.yesno:
                self.uix.logout()

class Slideshow():
    def __init__(self,listl,layout):
        self.listpix = listl
        self.current = 0
        self.l = QHBoxLayout()
        self.leftbut = QPushButton("<")
        self.leftbut.clicked.connect(self.left)
        self.rightbut = QPushButton(">")
        self.rightbut.clicked.connect(self.right)
        self.l.addStretch()
        self.l.addWidget(self.leftbut)
        self.labell = QLabel()
        self.pixmapp = QPixmap(self.listpix[self.current]).scaled(450,450,Qt.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation)
        self.labell.setPixmap(self.pixmapp)
        self.l.addWidget(self.labell)
        self.l.addWidget(self.rightbut)
        self.l.addStretch()

        layout.addLayout(self.l)

    def right(self):
        if self.current + 1 <= len(self.listpix)-1:
            self.current += 1
            self.update()
        else:
            self.current = 0
            self.update()
        
    def left(self):
        if self.current - 1 >= 0 :
            self.current -= 1
            self.update()
        else:
            self.current = len(self.listpix)-1
            self.update()
    
    def update(self):
        self.pixmapp = QPixmap(self.listpix[self.current]).scaled(450,450,Qt.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation)
        self.labell.setPixmap(self.pixmapp)

class UI(QWidget):
    def __init__(self):
        super().__init__()
        self.logo = os.path.join(dir,"assets","photos","logo.png")
        self.msg = QMessageBox()
        self.msg.setWindowTitle("Message")
        self.msg.setWindowIcon(QIcon(self.logo))

        self.fontlist = []
        for i in os.listdir(os.path.join(dir,"assets","fonts")):
            if i.endswith(".ttf"):
                self.fontlist.append(i)
        if len(self.fontlist) < 1:
            self.fontlist.append("None")
        
        self.RestoreFiles()
        self.enc = Encryption(self)

        self.loginstate = False
        self.setWindowIcon(QIcon(self.logo))
        self.layout = QHBoxLayout()
        self.sidebar = QGroupBox()
        self.sidebar.setFixedWidth(200)
        self.sidel = QVBoxLayout()
        self.sidebar.setLayout(self.sidel)
        self.layout.addWidget(self.sidebar)

        self.setLayout(self.layout)
        self.sizes = ["10","20","30","40","50","60","70","80","90","100"]
        self.logopix = QPixmap(self.logo).scaled(30,30,Qt.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation)
        self.logol = QLabel()
        self.logol.setPixmap(self.logopix)

        #Home
        self.homewidget = QWidget()
        self.home = QVBoxLayout()
        self.homewidget.setLayout(self.home)
        self.homescroll = QScrollArea()
        self.homescroll.setWidgetResizable(True)
        self.homescroll.setFrameShape(QFrame.NoFrame)
        self.homescroll.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.homescroll.setWidget(self.homewidget)

        self.homeg = QGroupBox()
        self.layout.addWidget(self.homeg)
        self.homemain = QHBoxLayout()
        self.homemain.addStretch()
        self.homemain.addWidget(self.homescroll)
        self.homemain.addStretch()
        self.homeg.setLayout(self.homemain)
        self.htitle = QHBoxLayout()
        self.htitle.addStretch()
        self.home.addLayout(self.htitle)
        self.homet = QLabel(self.lang["welcome"][self.curlang])
        self.htitle.addWidget(self.logol)
        self.htitle.addWidget(self.homet)
        self.htitle.addStretch()

        self.slideshows1 = QHBoxLayout()
        self.slideshows1.addStretch()
        self.slidel1 = QLabel(self.lang["about1"][self.curlang])
        self.home.addWidget(self.slidel1)
        self.slidel1.setWordWrap(True)
        self.setsize(self.slidel1,20)
        self.home.addLayout(self.slideshows1)
        self.slide1 = Slideshow([os.path.join(dir,"assets","photos","brokepass.png"),os.path.join(dir,"assets","photos","brokepass2.png"),os.path.join(dir,"assets","photos","brokepass3.png")],self.slideshows1)
        self.slideshows1.addStretch()

        self.home.addWidget(QLabel("\n"))
        self.slideshows2 = QHBoxLayout()
        self.slideshows2.addStretch()
        self.slidel2 = QLabel(self.lang["about2"][self.curlang])
        self.slidel2.setWordWrap(True)
        self.setsize(self.slidel2,20)
        self.home.addWidget(self.slidel2)
        self.home.addLayout(self.slideshows2)
        self.slide2 = Slideshow([os.path.join(dir,"assets","photos","afs.png"),os.path.join(dir,"assets","photos","notes.png"),os.path.join(dir,"assets","photos","brokepass.png")],self.slideshows2)
        self.slideshows2.addStretch()

        self.home.addWidget(QLabel("\n"))
        self.slideshows3 = QHBoxLayout()
        self.slideshows3.addStretch()
        self.slidel3 = QLabel(self.lang["about3"][self.curlang])
        self.slidel3.setWordWrap(True)
        self.setsize(self.slidel3,20)
        self.home.addWidget(self.slidel3)
        self.home.addLayout(self.slideshows3)
        self.slide3 = Slideshow([os.path.join(dir,"assets","photos","tt.png"),os.path.join(dir,"assets","photos","gh.png"),os.path.join(dir,"assets","photos","dc.png")],self.slideshows3)
        self.slideshows3.addStretch()
        self.home.addStretch()
        self.homescroll.setMinimumWidth(self.homescroll.width()+100)

        #Passwords
        self.maing = QGroupBox()
        self.layout.addWidget(self.maing)
        self.main = QHBoxLayout()
        self.main.addStretch()
        self.maing.setLayout(self.main)

        self.buts = QHBoxLayout()
        self.buts.addStretch()
        self.logopass = QLabel()
        self.logopass.setPixmap(QPixmap(self.logo).scaled(30,30,Qt.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation))

        self.passmain = QVBoxLayout()
        self.main.addLayout(self.passmain)
        self.passmain.addLayout(self.buts)
        self.titlel = QLabel(f"Broke Pass - {self.lang["pass"][self.curlang]}")
        self.setWindowTitle("Broke Pass")
        self.createbut = QPushButton(self.lang["create"][self.curlang])
        self.createbut.clicked.connect(lambda:self.adddialogbox.show())
        self.buts.addWidget(self.logopass)
        self.buts.addWidget(self.titlel)
        self.buts.addWidget(self.createbut)
        self.buts.addStretch()

        self.passabout = QLabel(self.lang["about4"][self.curlang])
        self.passabout.setWordWrap(True)
        self.passmain.addWidget(self.passabout)

        self.searchl = QHBoxLayout()
        self.searchline = QLineEdit()
        self.searchline.setPlaceholderText(self.lang["search1"][self.curlang])
        self.searchl.addWidget(self.searchline)
        self.searchbut = QPushButton(self.lang["search2"][self.curlang])
        self.searchbut.clicked.connect(self.addpasswords)
        self.searchl.addWidget(self.searchbut)
        self.passmain.addLayout(self.searchl)

        self.passwidget = QWidget()
        self.passl = QVBoxLayout()
        self.passwidget.setLayout(self.passl)
        self.passscroll = QScrollArea()
        self.passscroll.setWidgetResizable(True)
        self.passscroll.setFrameShape(QFrame.NoFrame)
        self.passscroll.setWidget(self.passwidget)
        self.passmain.addWidget(self.passscroll)
        self.main.addStretch()

        #About
        self.aboutwidget = QWidget()
        self.about = QVBoxLayout()
        self.aboutwidget.setLayout(self.about)
        self.aboutscroll = QScrollArea()
        self.aboutscroll.setWidgetResizable(True)
        self.aboutscroll.setFrameShape(QFrame.NoFrame)
        self.aboutscroll.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.aboutscroll.setWidget(self.aboutwidget)

        self.aboutg = QGroupBox()
        self.aboutg.hide()
        self.layout.addWidget(self.aboutg)
        self.aboutmain = QHBoxLayout()
        self.aboutmain.addStretch()
        self.aboutmain.addWidget(self.aboutscroll)
        self.aboutmain.addStretch()
        self.aboutg.setLayout(self.aboutmain)

        self.aboutlog = QLabel()
        self.aboutlog.setPixmap(self.logopix)
        self.abouttitle = QHBoxLayout()
        self.abouttitle.addStretch()
        self.about.addLayout(self.abouttitle)
        self.aboutt = QLabel(f"Broke Pass - {self.lang["about"][self.config["lang"]]}")
        self.abouttitle.addWidget(self.aboutlog)
        self.abouttitle.addWidget(self.aboutt)
        self.abouttitle.addStretch()

        self.about1 = QLabel(self.lang["aboutpage"][self.config["lang"]],alignment=Qt.AlignHCenter)
        self.about1.setWordWrap(True)
        self.about.addWidget(self.about1)

        self.about2 = QLabel(self.lang["aboutpage2"][self.config["lang"]],alignment=Qt.AlignHCenter)
        self.about2.setWordWrap(True)
        self.about.addWidget(self.about2)

        self.tiktokbut = QPushButton("My TikTok")
        self.tiktokbut.clicked.connect(lambda:opensite("tiktok.com/@br0ke.tech"))
        self.butsabout = QHBoxLayout()
        self.about.addLayout(self.butsabout)
        self.butsabout.addWidget(self.tiktokbut)

        self.githubbut = QPushButton("My GitHub")
        self.githubbut.clicked.connect(lambda:opensite("github.com/broke-tech"))
        self.butsabout.addWidget(self.githubbut)

        self.about.addWidget(QLabel("@br0ke.tech"),alignment=Qt.AlignRight)

        self.about.addStretch()
        self.aboutscroll.setMinimumWidth(self.aboutscroll.width()+100)
        self.aboutscroll.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        #updates
        self.updateswidget = QWidget()
        self.updates = QVBoxLayout()
        self.updateswidget.setLayout(self.updates)
        self.updatesscroll = QScrollArea()
        self.updatesscroll.setWidgetResizable(True)
        self.updatesscroll.setFrameShape(QFrame.NoFrame)
        self.updatesscroll.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.updatesscroll.setWidget(self.updateswidget)

        self.updatesg = QGroupBox()
        self.updatesg.hide()
        self.layout.addWidget(self.updatesg)
        self.updatesmain = QHBoxLayout()
        self.updatesmain.addStretch()
        self.updatesmain.addWidget(self.updatesscroll)
        self.updatesmain.addStretch()
        self.updatesg.setLayout(self.updatesmain)

        self.updateslog = QLabel()
        self.updateslog.setPixmap(self.logopix)
        self.updatestitle = QHBoxLayout()
        self.updatestitle.addStretch()
        self.updates.addLayout(self.updatestitle)
        self.updatest = QLabel(f"Broke Pass - {self.lang["updates"][self.config["lang"]]}")
        self.updatestitle.addWidget(self.updateslog)
        self.updatestitle.addWidget(self.updatest)
        self.updatestitle.addStretch()

        self.notavailableg = QGroupBox()
        self.notavailablel = QVBoxLayout()
        self.notavailableg.setLayout(self.notavailablel)
        self.updates.addWidget(self.notavailableg)
        self.notavailablem = QLabel(self.lang["latest"][self.config["lang"]],alignment=Qt.AlignHCenter)
        self.notavailablem.setWordWrap(True)
        self.setsize(self.notavailablem,30)
        self.notavailablel.addWidget(self.notavailablem)
        self.notavailablel.addWidget(QLabel(f"v{version}",alignment=Qt.AlignHCenter))
        self.notavailablenotes = QLabel(f"\n{self.lang["notes"][self.config["lang"]]}:\n{availablenotes}",alignment=Qt.AlignHCenter)
        self.notavailablenotes.setWordWrap(True)
        self.notavailablel.addWidget(self.notavailablenotes)

        self.availableg = QGroupBox()
        self.availablel = QVBoxLayout()
        self.availableg.setLayout(self.availablel)
        self.updates.addWidget(self.availableg)
        self.availablem = QLabel(self.lang["availableup"][self.config["lang"]],alignment=Qt.AlignHCenter)
        self.availablem.setWordWrap(True)
        self.setsize(self.availablem,30)
        self.availablel.addWidget(self.availablem)
        self.availablel.addWidget(QLabel(f"v{versionup}",alignment=Qt.AlignHCenter))
        self.availablenotes = QLabel(f"\n{self.lang["notes"][self.config["lang"]]}:\n{availablenotes}",alignment=Qt.AlignHCenter)
        self.availablenotes.setWordWrap(True)
        self.availablel.addWidget(self.availablenotes)
        self.availablebuts = QHBoxLayout()
        self.availablel.addLayout(self.availablebuts)

        self.upgithub = QPushButton("Get from GitHub")
        self.upgithub.clicked.connect(lambda:opensite("github.com/broke-tech/broke-pass/releases/latest"))
        self.upbroke = QPushButton("OTA update with Updater")
        self.upbroke.clicked.connect(lambda: self.messagebox("Run brokeupdater.exe and follow the instructions"))
        self.availablebuts.addStretch()
        self.availablebuts.addWidget(self.upbroke)
        self.availablebuts.addWidget(self.upgithub)
        self.availablebuts.addStretch()

        self.updategen = QLabel(f"Current version {version}",alignment=Qt.AlignRight)
        self.setsize(self.updategen,15)

        self.updates.addStretch()
        self.updates.addSpacerItem(QSpacerItem(0,50))
        self.updates.addWidget(self.updategen)
        self.updatesscroll.setMinimumWidth(self.updatesscroll.width()+100)
        self.updatesscroll.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        #Settings
        self.setg = QGroupBox()
        self.setg.hide()
        self.layout.addWidget(self.setg)
        self.settingslog = QLabel()
        self.settingslog.setPixmap(self.logopix)

        self.setwidget = QWidget()
        self.setl = QVBoxLayout()
        self.setwidget.setLayout(self.setl)
        self.setscroll = QScrollArea()
        self.setscroll.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.setscroll.setWidgetResizable(True)
        self.setscroll.setFrameShape(QFrame.NoFrame)
        self.setscroll.setWidget(self.setwidget)

        self.setmain = QHBoxLayout()
        self.setmain.addStretch()
        self.setmain.addWidget(self.setscroll)
        self.setg.setLayout(self.setmain)
        self.settitle = QHBoxLayout()
        self.setl.addLayout(self.settitle)
        self.settitle.addStretch()
        self.settitle.addWidget(self.settingslog)
        self.settitle.addWidget(QLabel(f"Broke Pass - {self.lang["setting"][self.config["lang"]]}"),alignment=Qt.AlignHCenter)
        self.settitle.addStretch()

        self.setl.addWidget(QLabel(f"\n{self.lang["appearance"][self.config["lang"]]}"),alignment=Qt.AlignHCenter)
        self.displayset = SettingCombo(self.lang["displaymode"][self.config["lang"]],self.lang["displaywarn"][self.config["lang"]],self.setl,"mode",[f"0 - {self.lang["dark"][self.config["lang"]]}",f"1 - {self.lang["light"][self.config["lang"]]}"],self)

        self.fontl = QHBoxLayout()
        self.setl.addLayout(self.fontl)
        self.fontcombo = QComboBox()
        self.fontcombo.addItems(self.fontlist)
        if os.path.exists(os.path.join(dir,"assets","fonts",self.curfont)):
            self.fontcombo.setCurrentText(self.curfont)
        else:
            self.fontcombo.setCurrentText(self.fontlist[0])
            self.curfont = self.fontlist[0]
            self.changefont()
        self.fontcombo.currentTextChanged.connect(self.changefont)
        self.fontl.addWidget(QLabel(self.lang["fontmode"][self.config["lang"]]))
        self.fontl.addWidget(self.fontcombo)
        self.fontdesc = QLabel(f"{self.lang["fontwarn"][self.config["lang"]]}\n")
        self.fontdesc.setWordWrap(True)
        self.setsize(self.fontdesc,15)
        self.setl.addWidget(self.fontdesc)
        
        self.languagel = QHBoxLayout()
        self.setl.addLayout(self.languagel)
        self.languagecombo = QComboBox()
        self.languagecombo.addItems(self.lang["langs"])
        self.languagecombo.setCurrentText(self.config["lang"])
        self.languagecombo.currentTextChanged.connect(self.changelang)
        self.languagel.addWidget(QLabel(self.lang["langmode"][self.config["lang"]]))
        self.languagel.addWidget(self.languagecombo)
        self.langdesc = QLabel(f"{self.lang["langwarn"][self.config["lang"]]}\n")
        self.langdesc.setWordWrap(True)
        self.setsize(self.langdesc,15)
        self.setl.addWidget(self.langdesc)
        
        self.setl.addWidget(QLabel(f"\n{self.lang["security"][self.config["lang"]]}"),alignment=Qt.AlignHCenter)
        self.hideset = SettingCombo(self.lang["passstate"][self.config["lang"]],self.lang["passwarn"][self.config["lang"]],self.setl,"hide",[f"0 - {self.lang["shown"][self.config["lang"]]}",f"1 - {self.lang["hidden"][self.config["lang"]]}"],self)
        self.passwordset = SettingCombo(self.lang["searchset"][self.config["lang"]],self.lang["searchwarn"][self.config["lang"]],self.setl,"search",[f"0 - {self.lang["websitesonly"][self.config["lang"]]}",f"1 - {self.lang["websitesandpasswords"][self.config["lang"]]}"],self)
        self.setl.addWidget(QLabel(f"\nUSER SETTINGS"),alignment=Qt.AlignHCenter)
        self.fileset = SettingCombo(self.lang["filelocation"][self.config["lang"]],self.lang["filewarn"][self.config["lang"]],self.setl,"file",[f"0 - {self.lang["fixedlocation"][self.config["lang"]]}",f"1 - {self.lang["previouslyused"][self.config["lang"]]}", f"2 - {self.lang["chooseeachtime"][self.config["lang"]]}"],self)

        self.usernamel = QHBoxLayout()
        self.setl.addLayout(self.usernamel)
        self.username = QLineEdit()
        self.usernamebut = QPushButton(self.lang["change"][self.config["lang"]])
        self.usernamebut.clicked.connect(self.changeusername)
        self.usernamel.addWidget(QLabel(self.lang["userset"][self.config["lang"]]))
        self.usernamel.addWidget(self.username)
        self.usernamel.addWidget(self.usernamebut)

        self.passwordmasterl = QHBoxLayout()
        self.setl.addLayout(self.passwordmasterl)
        self.passwordmaster = QLineEdit()
        self.passwordmasterbut = QPushButton(self.lang["change"][self.config["lang"]])
        self.passwordmasterbut.clicked.connect(self.changemaster)
        self.passwordmasterl.addWidget(QLabel(self.lang["masterset"][self.config["lang"]]))
        self.passwordmasterl.addWidget(self.passwordmaster)
        self.passwordmasterl.addWidget(self.passwordmasterbut)
        self.masterdesc = QLabel(f"{self.lang["masterwarn"][self.config["lang"]]}\n")
        self.masterdesc.setWordWrap(True)
        self.setsize(self.masterdesc,15)
        self.setl.addWidget(self.masterdesc)

        self.setl.addWidget(QLabel(f"\n{self.lang["data"][self.config["lang"]]}"),alignment=Qt.AlignHCenter)
        self.exportl = QHBoxLayout()
        self.setl.addLayout(self.exportl)
        self.exportbut = QPushButton(self.lang["export"][self.config["lang"]])
        self.exportbut.clicked.connect(self.enc.export)
        self.exportl.addWidget(QLabel(f"{self.lang["export"][self.config["lang"]]} {self.lang["decpass"][self.config["lang"]]}: "))
        self.exportl.addWidget(self.exportbut)

        self.importl = QHBoxLayout()
        self.setl.addLayout(self.importl)
        self.importbut = QPushButton(self.lang["import"][self.config["lang"]])
        self.importbut.clicked.connect(self.enc.importpass)
        self.importl.addWidget(QLabel(f"{self.lang["import"][self.config["lang"]]} {self.lang["decpass"][self.config["lang"]]}: "))
        self.importl.addWidget(self.importbut)
        self.importdesc = QLabel(f"{self.lang["decpasswarn"][self.config["lang"]]}\n")
        self.importdesc.setWordWrap(True)
        self.setsize(self.importdesc,15)
        self.setl.addWidget(self.importdesc)  
        self.settingslocation = QLabel(self.lang["current"][self.config["lang"]])
        self.setsize(self.settingslocation,17)
        self.setl.addWidget(self.settingslocation)

        self.setl.addStretch()

        self.versionl = QHBoxLayout()
        self.setl.addSpacerItem(QSpacerItem(0,100))
        self.setl.addLayout(self.versionl)
        self.versionl.addWidget(QLabel(f"with love\nby {developer}"))
        self.versionl.addStretch()
        self.versionl.addWidget(QLabel(f"Broke Pass\nversion {version}",alignment=Qt.AlignRight))
        self.setmain.addStretch()
        self.setscroll.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.setscroll.setMinimumWidth(self.setscroll.width()+100)

        #Sections
        self.sectionlpix = QPixmap(self.logo).scaled(40,40,Qt.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation)
        self.sectionlogo = QLabel()
        self.sectionlogo.setPixmap(QPixmap(os.path.join(dir,"assets","photos","logobig.png")).scaled(150,50,Qt.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation))
        self.sectiontitle = QHBoxLayout()
        self.sectiontitle.addWidget(self.sectionlogo)
        self.sectiontitle.addStretch()

        if updateavailable:
            up = " •"
        else:
            up = ""
        
        self.sidel.addLayout(self.sectiontitle)
        self.sectionbuts = list()
        for i in [[self.lang["home"][self.config["lang"]],"h"],[self.lang["passwords"][self.config["lang"]],"p"],[self.lang["about"][self.config["lang"]],"a"],[self.lang["setting"][self.config["lang"]],"s"]]:
            a = Button(i[0],i[1],self)
            self.sectionbuts.append(a)
        self.sidel.addStretch()
        for i in [[f"{self.lang["updates"][self.config["lang"]]}{up}","u"],["Log Out","l"]]:
            a = Button(i[0],i[1],self)
            self.sectionbuts.append(a)

        #dialog
        self.dialogbox = QDialog()
        self.dialogbox.setWindowIcon(QIcon(self.logo))
        self.butts = QHBoxLayout()
        self.accepted = QPushButton("")
        self.rejected = QPushButton("")
        self.accepted.clicked.connect(lambda: self.stated(True))
        self.rejected.clicked.connect(lambda: self.stated(False))
        self.butts.addStretch()
        self.butts.addWidget(self.accepted)
        self.butts.addWidget(self.rejected)
        self.dlayout = QVBoxLayout()
        self.dmessage = QLabel("")
        self.dmessage.setWordWrap(True)
        self.dlayout.addWidget(self.dmessage)
        self.dlayout.addLayout(self.butts)
        self.dialogbox.setLayout(self.dlayout)

        #Login
        self.logolog = QLabel()
        self.logolog.setPixmap(self.logopix)

        self.logindialogbox = QDialog()
        self.logindialogbox.setWindowIcon(QIcon(self.logo))
        self.loginbutts = QHBoxLayout()
        self.loginaccepted = QPushButton(self.lang["login"][self.curlang])
        self.loginrejected = QPushButton(self.lang["cancel"][self.curlang])
        self.loginaccepted.clicked.connect(lambda: self.logincheck(True))
        self.loginrejected.clicked.connect(lambda: self.logincheck(False))
        self.loginbutts.addStretch()
        self.loginbutts.addWidget(self.loginaccepted)
        self.loginbutts.addWidget(self.loginrejected)
        self.logindlayout = QVBoxLayout()
        self.logindusertrue = QVBoxLayout()
        self.loginduserg = QGroupBox()
        self.loginduserg.setLayout(self.logindusertrue)

        self.logindnousertrue = QVBoxLayout()
        self.logindnouserg = QGroupBox()
        self.logindnouserg.setLayout(self.logindnousertrue)
        self.logindnousertrue.addWidget(QLabel(self.lang["nopass"][self.curlang]))
    
        self.logindtitle = QHBoxLayout()
        self.logindlayout.addLayout(self.logindtitle)
        self.logindtitle.addWidget(self.logolog)
        self.logindtitle.addWidget(QLabel("Broke Pass - LOGIN"))

        self.logindabout = QPushButton(self.lang["firsttime"][self.curlang])
        self.logindabout.clicked.connect(lambda: self.messagebox(self.lang["firsttut"][self.curlang]))
        self.logindtitle.addStretch()
        self.logindtitle.addWidget(self.logindabout)

        self.logindlayout.addWidget(self.loginduserg)
        self.logindlayout.addWidget(self.logindnouserg)
        self.logindmessage = QLabel(f"",alignment=Qt.AlignHCenter)
        self.loginline = QLineEdit()
        self.loginline.setPlaceholderText(self.lang["master password"][self.curlang]+"...")
        self.loginline.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        self.loginlocation = QLabel(f"{self.lang["current"][self.curlang]}")
        self.setsize(self.loginlocation,17)
        
        self.logindusertrue.addWidget(self.logindmessage)
        self.logindusertrue.addWidget(self.loginline)
        self.logindusertrue.addWidget(self.loginlocation)
        self.logindusertrue.addLayout(self.loginbutts)
        self.logindialogbox.setLayout(self.logindlayout)

        self.logindlayout.addStretch()
        self.loginduser = QHBoxLayout()
        self.logindlayout.addLayout(self.loginduser)
        self.logindusermsg = QLabel(self.lang["openorcreate"][self.curlang][1])
        self.logindother = QPushButton(self.lang["openorcreate"][self.curlang][0])
        self.logindother.clicked.connect(self.openother)
        self.setsize(self.logindusermsg,15)
        self.loginduser.addWidget(self.logindother)
        self.loginduser.addWidget(self.logindusermsg)
        
        self.logindnewmsg = QLabel(self.lang["openorcreate"][self.curlang][3])
        self.logindnewuser = QPushButton(self.lang["openorcreate"][self.curlang][2])
        self.logindnewuser.clicked.connect(lambda: self.newuserdialogbox.show())
        self.setsize(self.logindnewmsg,15)
        self.loginduser.addWidget(self.logindnewuser)
        self.loginduser.addWidget(self.logindnewmsg)

        self.loginduser.addStretch()
        self.logindialogbox.setWindowTitle("Broke Pass - LOGIN")
        self.logindialogbox.setFixedSize(0,0)

        self.GetFileLocation()
        self.enc.changeuser(self.filelocation,self)

        #Add pass
        self.adddialogbox = QDialog()
        self.addlayout = QFormLayout()
        self.adddialogbox.setWindowIcon(QIcon(self.logo))
        self.addaccepted = QPushButton(self.lang["create"][self.curlang])
        self.addaccepted.clicked.connect(self.create)
        self.addrejected = QPushButton(self.lang["cancel"][self.curlang])
        self.addrejected.clicked.connect(lambda: self.adddialogbox.hide())
        self.adddmessage = QLabel(self.lang["newentry"][self.curlang])
        self.addwebsiteline = QLineEdit()
        self.addwebsiteline.setPlaceholderText(self.lang["enterweb"][self.curlang])
        self.addpasswordline = QLineEdit()
        self.addpasswordline.setPlaceholderText(self.lang["enterpassword"][self.curlang])
        self.addgenerate = QPushButton(self.lang["generate"][self.curlang])
        self.addgenerate.clicked.connect(lambda: self.addpasswordline.setText(''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=12))))
        self.addlayout.addRow(self.adddmessage)
        self.addlayout.addRow(self.addwebsiteline)
        self.addlayout.addRow(self.addgenerate,self.addpasswordline)
        self.addlayout.addRow(self.addaccepted)
        self.adddialogbox.setLayout(self.addlayout)

        self.newuserdialogbox = QDialog()
        self.newuserlayout = QFormLayout()
        self.newuserdialogbox.setWindowIcon(QIcon(self.logo))
        self.newuseraccepted = QPushButton(self.lang["create"][self.curlang])
        self.newuseraccepted.clicked.connect(self.enc.createnewuser)
        self.newuserrejected = QPushButton(self.lang["cancel"][self.curlang])
        self.newuserrejected.clicked.connect(lambda: self.newuserdialogbox.hide())
        self.newusermessage = QLabel(self.lang["newuser"][self.curlang])
        self.newusername = QLineEdit()
        self.newusername.setPlaceholderText(self.lang["user name"][self.curlang])
        self.newuserpasswordline = QLineEdit()
        self.newuserpasswordline.setPlaceholderText(self.lang["master password"][self.curlang])
        self.newusergenerate = QPushButton(self.lang["generate"][self.curlang])
        self.newusergenerate.clicked.connect(lambda: self.newuserpasswordline.setText(''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=12))))
        
        self.newuserwarn = QLabel(self.lang["master"][self.curlang])
        self.newuserwarn.setWordWrap(True)
        self.setsize(self.newuserwarn,15)
        
        self.newuserlayout.addRow(self.newusermessage)
        self.newuserlayout.addRow(self.newusername)
        self.newuserlayout.addRow(self.newusergenerate,self.newuserpasswordline)
        self.newuserlayout.addRow(self.newuserwarn)
        self.newuserlayout.addRow(self.newuseraccepted)
        self.newuserdialogbox.setLayout(self.newuserlayout)

        #styling
        self.GetUpdate()
        self.appstyle()

    def RestoreFiles(self):
        with open(os.path.join(dir,"assets","config.json"),encoding="utf-8") as file:
            self.config = json.load(file)
        try:
            self.curfont = self.config["font"]
        except:
            self.config["font"] = self.fontlist[0]
            with open(os.path.join(dir,"assets","config.json"),"w",encoding="utf-8") as file:
                json.dump(self.config,file)

        try:
            self.curlang = self.config["lang"]
        except:
            self.config["lang"] = "english"
            with open(os.path.join(dir,"assets","config.json"),"w",encoding="utf-8") as file:
                json.dump(self.config,file)

        with open(os.path.join(dir,"assets","style.json"),encoding="utf-8") as file:
            self.styles = json.load(file)
        with open(os.path.join(dir,"assets","lang.json"),encoding="utf-8") as file:
            self.lang = json.load(file)
        
        self.curlang = self.config["lang"]
        self.curfont = self.config["font"]

    def filtersearch(self,password):
        if self.config["search"] == "0":
            if self.searchline.text().lower() in password.split(" ")[0].lower():
                return True
        if self.config["search"] == "1":
            if self.searchline.text().lower() in password.split(" ")[1].lower() or self.searchline.text().lower() in password.split(" ")[0].lower():
                return True
        return False
    
    def openother(self):
        location = QFileDialog.getOpenFileName(self,"Select the passwords file","","Broke Pass (*.bpass)")[0]
        self.enc.changeuser(location,self)
        
    def logincheck(self,state):
        if state == True:
            if self.loginline.text() == self.enc.masterpassword:
                self.addpasswords()
                if self.config["file"] == "1":
                    self.config["filelocation"] = self.filelocation
                with open(os.path.join(dir,"assets","config.json"),"w",encoding="utf-8") as file:
                    json.dump(self.config,file)
                self.loginstate = True
                self.logindialogbox.hide()
                self.searchline.clear()
                self.show()
                self.sectionbuts[0].change()
                self.loginline.clear()
            else:
                self.messagebox("Incorrect password")
        elif state == False:
            sys.exit()
    
    def logout(self):
        self.loginstate = False
        self.enc.changeuser(self.filelocation,self)
        self.searchline.clear()
        self.loginline.clear()
        self.logindialogbox.show()
        self.hide()
        
    def changemaster(self):
        if len(self.passwordmaster.text()) > 0 and " " not in self.passwordmaster.text():
            self.dialog(self.lang["sure"][self.curlang],self.lang["masterchange"][self.curlang],self.lang["yes"][self.curlang],self.lang["no"][self.curlang])
            if self.yesno:
                self.enc.masterpassword = self.passwordmaster.text()
                self.enc.encryptsave()
        else:
            self.messagebox(self.lang["masterspaces"][self.curlang])

    def changeusername(self):
        if len(self.username.text()) > 0 and " " not in self.username.text():
            self.dialog(self.lang["sure"][self.curlang],self.lang["userchange"][self.curlang],self.lang["yes"][self.curlang],self.lang["no"][self.curlang])
            if self.yesno:
                self.enc.user = self.username.text()
                self.enc.encryptsave()
        else:
            self.messagebox(self.lang["userspaces"][self.curlang])

    def changelang(self):
        self.config["lang"] = self.languagecombo.currentText()
        self.curlang = self.config["lang"]
        with open(os.path.join(dir,"assets","config.json"),"w",encoding="utf-8") as file:
            json.dump(self.config,file)
        self.messagebox(self.lang["restartapply"][self.curlang])
    
    def changefont(self):
        self.config["font"] = self.fontcombo.currentText()
        self.curfont = self.config["font"]
        with open(os.path.join(dir,"assets","config.json"),"w",encoding="utf-8") as file:
            json.dump(self.config,file)
        self.setfont()

    def refresh_ui(self): #By chatGPT
        app.processEvents()
        for widget in app.allWidgets():
            widget.style().unpolish(widget)
            widget.style().polish(widget)
            widget.update()
            
    def stated(self,s):
        self.yesno = s
        self.dialogbox.hide()

    def dialog(self,title,command,yestext,notext):
        self.dialogbox.setWindowTitle(title)
        self.dmessage.setText(command)
        self.accepted.setText(yestext)
        self.rejected.setText(notext)
        self.yesno = False
        self.dialogbox.exec()

    def messagebox(self,message):
        self.msg.setText(message)
        self.msg.exec()

    def addpasswords(self):
        self.clear_layout(self.passl)
        self.enc.decrpasswords.sort()
        addsfav = []
        adds = [] #[1:]
        for i in self.enc.decrpasswords:
            try:
                if i.split(" ")[2] == "f":
                    if len(self.searchline.text()) > 0:
                        if self.filtersearch(i):
                            addsfav.append([i.split(" ")[0],i.split(" ")[1],i.split(" ")[2]])
                    else:
                        addsfav.append([i.split(" ")[0],i.split(" ")[1],i.split(" ")[2]])
                else:
                    if len(self.searchline.text()) > 0:
                        if self.filtersearch(i):
                            adds.append([i.split(" ")[0],i.split(" ")[1],i.split(" ")[2]])
                    else:
                        adds.append([i.split(" ")[0],i.split(" ")[1],i.split(" ")[2]])
            except:
                if len(self.searchline.text()) > 0:
                        if self.filtersearch(i):
                            adds.append([i.split(" ")[0],i.split(" ")[1],"n"])
                else:
                    adds.append([i.split(" ")[0],i.split(" ")[1],"n"])

        for i in addsfav:
            pwd = Pwd(self,i[0],i[1],i[2])
        for i in adds:
            pwd = Pwd(self,i[0],i[1],i[2])
        self.passl.addStretch()
    
    def appstyle(self):
        for i in [self,app,self.msg,self.dialogbox]:
            i.setStyleSheet("")
        if self.config["mode"] == "0":
            self.setmodeblack()
            for i in [self,app,self.msg,self.dialogbox]:
                i.setStyleSheet(self.styles["styleblack"])
        elif self.config["mode"] == "1":
            self.setmodewhite()
            for i in [self,app,self.msg,self.dialogbox]:
                i.setStyleSheet(self.styles["stylewhite"])
        for i in self.sectionbuts:
            if i.id == 's':
                i.change()
        self.tiktokbut.setIcon(QIcon(os.path.join(dir,"assets","icons",f"tiktok{self.config["mode"]}.png")))
        self.githubbut.setIcon(QIcon(os.path.join(dir,"assets","icons",f"github{self.config["mode"]}.png")))

        self.logindother.setStyleSheet(self.styles["textbut"])
        self.logindabout.setStyleSheet(self.styles["textbut"])
        self.logindnewuser.setStyleSheet(self.styles["textbut"])
        self.createbut.setStyleSheet(self.styles["colorbut"])
        self.setfont()

    def GetUpdate(self):
        self.notavailableg.hide()
        self.availableg.hide()
        if updateavailable:
            self.availableg.show()
        else:
            self.notavailableg.show()

    def create(self):
        if len(self.addwebsiteline.text()) != 0 and len(self.addpasswordline.text()) != 0:
            for i in self.enc.decrpasswords:
                if i.split(" ")[0] == self.addwebsiteline.text():
                    self.messagebox(self.lang["alreadyentry"][self.curlang])
                    return False
            if " " in self.addwebsiteline.text() or " " in self.addpasswordline.text():
                self.messagebox(self.lang["yetanotherspace"][self.curlang])
                return False
            if self.addwebsiteline.text() == "brokeuser" or self.addwebsiteline.text() == "brokepassword":
                self.messagebox("You can't name your website 'brokeuser' or 'brokepassword'.")
                return False
            self.enc.decrpasswords.append(f"{self.addwebsiteline.text()} {self.addpasswordline.text()} n")
            self.enc.encryptsave()
            self.addpasswords()
            self.addwebsiteline.clear()
            self.addpasswordline.clear()
            self.adddialogbox.hide()
        else:
            self.messagebox(self.lang["all fields"][self.curlang])

    def clear_layout(self,layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clear_layout(item.layout())
    
    def setfont(self):
        font_path = os.path.join(dir,"assets","fonts",self.curfont)
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            app.setFont(QFont(font_family,11))
        else:
            self.messagebox("Font not found.")
        self.refresh_ui()

    def GetFileLocation(self):
        if self.config["file"] == "2":
            self.filelocation = os.path.join(dir,"assets","default.bpass")
        elif self.config["file"] == "0":
            if os.path.exists(self.config["filelocation"]):
                self.filelocation = self.config["filelocation"]
            elif self.config["filelocation"] == "default":
                self.filelocation = os.path.join(dir,"assets","default.bpass")
            else:
                self.messagebox(f"Your passwords file was not found\nin the fixed location. Changed the file option to {self.lang["chooseeachtime"][self.curlang]}")
                self.config["file"] = "2"
                with open(os.path.join(dir,"assets","config.json"),"w",encoding="utf-8") as file:
                    json.dump(self.config,file)
                sys.exit()
        elif self.config["file"] == "1":
            if os.path.exists(self.config["filelocation"]):
                self.filelocation = self.config["filelocation"]
            elif self.config["filelocation"] == "default":
                self.filelocation = os.path.join(dir,"assets","default.bpass")
            else:
                self.messagebox(f"Your passwords file was not found\nin the fixed location. Changed the file option to {self.lang["chooseeachtime"][self.curlang]}")
                self.config["file"] = "2"
                with open(os.path.join(dir,"assets","config.json"),"w",encoding="utf-8") as file:
                    json.dump(self.config,file)
                sys.exit()

    def setmodeblack(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, Qt.black)
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, Qt.black)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor("#242424"))
        palette.setColor(QPalette.ButtonText, Qt.white)
        app.setPalette(palette)

    def setmodewhite(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, Qt.white)
        palette.setColor(QPalette.WindowText, Qt.black)
        palette.setColor(QPalette.Base, Qt.white)
        palette.setColor(QPalette.Text, Qt.black)
        palette.setColor(QPalette.Button, QColor("#959595"))
        palette.setColor(QPalette.ButtonText, Qt.black)
        app.setPalette(palette)

    def setsize(self,widget,size):
        widget.setStyleSheet(f"font-size: {size}px;")

    def semititle(self,title,layout):
        label = QLabel(title)
        label.setStyleSheet("color: #ffffff; font-size: 30px;")    
        layout.addWidget(QLabel())
        layout.addWidget(label,alignment=Qt.AlignLeft)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    ui = UI()
    ui.logindialogbox.show()
    app.exec()
