from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from pyqtProject import Ui_Dialog
import os
class cls_pyqtProject(QtWidgets.QDialog):
    def __init__(self):
        super(cls_pyqtProject, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        DocumentsPath = os.path.expanduser('~/Documents')
        DocumentsPath = DocumentsPath.replace('/', '\\')
        DocumentsPath = DocumentsPath + '\\'
        self.ui.txtlocation.setText(DocumentsPath)
        self.ui.pushButton.clicked.connect(self.selectLocation)
        self.ui.btnok.clicked.connect(self.okClick)
        self.ui.btncancle.clicked.connect(self.cancleClick)
        self.pName = ""
        self.pLocation = ""
        self.uifileName = ""
        self.pyfileName = ""
        self.classfileName = ""
        x = "vvvvv"

    def selectLocation(self):
        DocumentsPath = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        DocumentsPath = DocumentsPath.replace('/', '\\')
        DocumentsPath = DocumentsPath + '\\'
        self.ui.txtlocation.setText(DocumentsPath)
        x = "zzzzz"

    def okClick(self):
        self.pName = self.ui.txtprojectName.text()
        self.pLocation = self.ui.txtlocation.text()
        self.uifileName = self.ui.txtuifileName.text()
        self.pyfileName = self.ui.txtpyfileName.text()
        self.classfileName =self.ui.txtclassfileName.text()

        self.accept()

    def cancleClick(self):
        self.reject()