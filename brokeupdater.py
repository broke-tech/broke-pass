from PyQt5.QtCore import Qt,QProcess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,QSpacerItem, QLabel, QLineEdit, QComboBox,
    QPushButton, QProgressBar, QDialog,QTextEdit,QFileDialog,
    QGroupBox, QFormLayout, QMessageBox,QCheckBox)
from PyQt5.QtGui import QPalette, QColor, QFont,QFontDatabase
import sys
import os
from requests import get
import json
from random import randint
curdir = os.getcwd()
version = "1.0 BETA"

class UI(QWidget):
    def __init__(self):
        super().__init__()
        self.msg = QMessageBox()
        self.msg.setWindowTitle("Message")
        self.setMinimumWidth(400)
        self.setMaximumSize(0,0)

        self.layout = QVBoxLayout()
        self.layout.addStretch()
        self.setLayout(self.layout)
        self.layout.addWidget(QLabel("Broke Pass - Updater"),alignment=Qt.AlignHCenter)

        self.firstg = QGroupBox()
        self.firstl = QVBoxLayout()
        self.firstg.setLayout(self.firstl)
        self.layout.addWidget(self.firstg)

        self.directory = QLineEdit("")
        self.directory.setReadOnly(True)
        self.dirbut = QPushButton("Choose")
        self.dirbut.clicked.connect(self.openother)
        self.dirh = QHBoxLayout()
        self.firstl.addWidget(QLabel("Current Broke Pass directory"))
        self.firstl.addLayout(self.dirh)
        self.dirh.addWidget(self.directory)
        self.dirh.addWidget(self.dirbut)
        self.firstl.addSpacerItem(QSpacerItem(0,5))

        self.source = QLineEdit("github.com/broke-tech/broke-pass")
        self.source.setReadOnly(True)
        self.firstl.addWidget(QLabel("Update Source"))
        self.firstl.addWidget(self.source)
        self.firstl.addSpacerItem(QSpacerItem(0,5))

        self.keepl = QHBoxLayout()
        self.firstl.addLayout(self.keepl)
        self.keepl.addWidget(QLabel("Keep current settings"))
        self.keepl.addStretch()
        self.keep = QCheckBox()
        self.keep.setCheckState(True)
        self.keep.setTristate(False)
        self.keepl.addWidget(self.keep)
        self.firstl.addSpacerItem(QSpacerItem(0,5))

        self.firstbut = QPushButton("Update")
        self.firstbut.clicked.connect(self.UpdateBrokePass)
        self.firstl.addWidget(self.firstbut)
        
        self.secondg = QGroupBox()
        self.secondg.hide()
        self.secondl = QVBoxLayout()
        self.secondg.setLayout(self.secondl)
        self.layout.addWidget(self.secondg)
        
        self.statel = QLabel("Download in process...\nPlease don't close this window.")
        self.secondl.addWidget(self.statel)
        self.progress = QProgressBar()
        self.progress.setMinimum(0)
        self.progress.setMaximum(100)
        self.secondl.addWidget(self.progress)
        self.terminal = QTextEdit()
        self.terminal.setReadOnly(True)
        self.secondl.addWidget(self.terminal)
        self.secondl.addStretch()
        self.layout.addWidget(QLabel(f"Broke Pass Updater - v{version}"))
        self.layout.addStretch()

        self.worker = QProcess()
        self.worker.setWorkingDirectory(self.directory.text())
        self.worker.readyReadStandardOutput.connect(self.UpdateWorker)
        self.worker.errorOccurred.connect(self.UpdateWorker)
        self.worker.readyReadStandardError.connect(self.UpdateWorker)

        #dialog
        self.dialogbox = QDialog()
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

        self.appstyle()
    
    def appstyle(self):
        self.setmodeblack()
        for i in [self,app,self.msg,self.dialogbox]:
            i.setStyleSheet("QGroupBox { border : none; } QLineEdit { background-color: #242424; font-size: 15px; border-radius: 8px; padding: 4px; } QPushButton {background-color: #242424;color: #ffffff;padding: 5px;border-radius: 9px;font-size: 15px;}QPushButton:hover {background-color: #545454;color: #ffffff;padding: 5px;border-radius: 9px;font-size: 15px;}QLabel {font-size: 15px;}QTextEdit {font-size: 20px;}")

    def UpdateWorker(self):
        out = self.worker.readAllStandardOutput().data().decode().strip()
        if out:
            self.terminal.setText(out)

        err = self.worker.readAllStandardError().data().decode().strip()
        if err:
            self.terminal.setText(err)

        try:
            self.progress.setValue(int(out.split(" ")[0]))
        except:
            try:
                self.progress.setValue(int(err.split(" ")[0]))
            except:
                pass

    def openother(self):
        location = QFileDialog.getExistingDirectory()
        if location != "":
            if "brokepass.exe" not in os.listdir(location):
                self.dialog("Continue?","This folder might not contain Broke Pass! Choose anyway?","Yes","No")
                if self.yesno:
                    self.directory.setText(location)
            else:
                self.directory.setText(location)
    
    def messagebox(self,message):
        self.msg.setText(message)
        self.msg.exec()

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
        
    def UpdateFinish1(self):
        if os.path.getsize(os.path.join(self.directory.text(),self.filename)) > 20000000:
            self.worker.start(f'tar -xf "{os.path.join(self.directory.text(),self.filename)}" -C "{self.directory.text()}"')
            self.progress.setMaximum(0)
            self.worker.finished.disconnect()
            self.worker.finished.connect(self.UpdateFinish2)
            self.statel.setText("Installation in process...\nPlease don't close this window.")
            print("ok")
        else:
            self.dialog("Error","The downloaded file might be corrupted. Do you want to redownload it or use it (not recommended)","Redownload","Use")
            if self.yesno:
                self.UpdateBrokePass()
            else:
                self.worker.start(f'tar -xf "{os.path.join(self.directory.text(),self.filename)}" -C "{self.directory.text()}"')
                self.progress.setMaximum(0)
                self.worker.finished.disconnect()
                self.worker.finished.connect(self.UpdateFinish2)
                self.statel.setText("Installation in process...\nPlease don't close this window.")
    
    def UpdateFinish2(self):
        self.worker.finished.disconnect()
        self.progress.setMaximum(100)
        self.progress.setValue(100)
        if self.keep.checkState() == 2:
            with open(os.path.join(self.directory.text(),"assets","config.json"),"w",encoding="utf-8") as file:
                json.dump(self.config,file)
        os.remove(os.path.join(self.directory.text(), self.filename))
        self.statel.setText("Installation completed!\nYou can now close this window")
        self.terminal.setText("Update completed successfully!")

    def UpdateBrokePass(self):
        try:
            self.dialog("Continue?","This will overwrite your current Broke Pass installation. Please if you want to keep your config, check the appropriate box first! Continue?","Yes","No")
            if self.yesno:
                if self.directory.text() != "":
                    releasenotesurl = "https://raw.githubusercontent.com/broke-tech/broke-pass/refs/heads/main/releasenotes"
                    r = get(releasenotesurl)
                    if self.keep.checkState() == 2:
                        with open(os.path.join(self.directory.text(),"assets","config.json"),encoding="utf-8") as file:
                            self.config = json.load(file)
                    self.worker.setWorkingDirectory(self.directory.text())
                    source = self.source.text()+"/releases/latest/download/BrokePassWindows.zip"
                    self.firstg.hide()
                    self.secondg.show()
                    self.filename = f"tempbpupdate{randint(1000,9999)}.zip"
                    self.worker.start(f"curl -L -o {self.filename} {source}")
                    print("ok")
                    self.worker.finished.connect(self.UpdateFinish1)
                else:
                    self.messagebox("Please choose a valid directory first")
        except:
            self.messagebox("No internet connection!")

    def setmodeblack(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, Qt.black)
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, Qt.black)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor("#242424"))
        palette.setColor(QPalette.ButtonText, Qt.white)
        app.setPalette(palette)

    def setsize(self,widget,size):
        widget.setStyleSheet(f"font-size: {size}px;")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    ui = UI()
    ui.show()
    app.exec()
