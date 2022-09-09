from PyQt5 import QtWidgets
from LogoForm import Ui_MainWindow
import sys
import os
import shutil
import py7zr
from pyunpack import Archive
class cls_logoform(QtWidgets.QMainWindow):
    def __init__(self):
        super(cls_logoform, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.btncopy.clicked.connect(self.extractaC)


    def extractaC(self):
        cwd = os.getcwd()
        appDataPath = os.getenv('APPDATA')
        CCpath = os.path.join(appDataPath, "Ezapiya")
        destination_dir = CCpath + "\\"
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
        try:
            Archive('mingw64.7z').extractall(destination_dir)
            runFile = cwd + "\\stop_.exe"
            runFileDestination = appDataPath + "\\Ezapiya\\"
            shutil.copy(runFile, runFileDestination)
            self.ui.pushButton.setEnabled(True)
        except Exception as e:
            print(e)
    def CCCopy_function(self):
        print("Install Button Click")
        self.ui.pushButton.setEnabled(False)
        cwd = os.getcwd()
        OCpath = os.path.join(cwd, "MinGW")
        appDataPath = os.getenv('APPDATA')
        CCpath = os.path.join(appDataPath, "Ezapiya\\MinGW")
        #os.mkdir(CCpath)
        source_dir = OCpath+"\\"
        destination_dir = CCpath+"\\"
        print(source_dir)
        print(destination_dir)
        #shutil.copytree(OCpath, CCpath)

        self.copytreefun(source_dir, destination_dir)
        runFile = cwd + "\\stop_.exe"
        runFileDestination = appDataPath + "\\Ezapiya\\"
        shutil.copy(runFile, runFileDestination)
        self.ui.pushButton.setEnabled(True)

    def copytreefun(obj,srcDir, dst, symlinks=False, ignore=None):
        try:
            if not os.path.exists(dst):
                os.makedirs(dst)
            for item in os.listdir(srcDir):
                s = os.path.join(srcDir, item)
                d = os.path.join(dst, item)
                if os.path.isdir(s):
                    obj.copytreefun(s, d, symlinks, ignore)
                else:
                    if not os.path.exists(d) or os.stat(s).st_mtime - os.stat(d).st_mtime > 1:
                        shutil.copy2(s, d)
        except NameError:
            print(NameError)