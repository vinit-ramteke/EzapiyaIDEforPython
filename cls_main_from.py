import subprocess
import os
from subprocess import Popen, PIPE
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QDialog, QLineEdit, QFileSystemModel
import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from pip._vendor.pyparsing import Each

from mainForm import Ui_MainWindow
from SimplePythonEditor import SimplePythonEditor
from cls_SimplePythonProject import cls_SimplePythonProject
from cls_pyqtProject import cls_pyqtProject
import sqlite3
import icon_qrc
import glob

class cls_main_from(QtWidgets.QMainWindow):
    def __init__(self):
        super(cls_main_from, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.message_window_status = False
        self.tool_box_status = False
        self.project_window_status = False
        self.property_window_status = False


        self.findLineEdit = QLineEdit(self)
        self.findLineEdit.setFixedWidth(200)
        self.findLineEdit.setFixedHeight(30)
        self.findLineEdit.setFont(QFont('SansSerif', 14))
        self.findLineEdit.setStyleSheet("color: rgb(255, 255, 255);")
        self.ui.toolBar.insertWidget(self.ui.actionFind, self.findLineEdit)

        self.replaceLineEdit = QLineEdit(self)
        self.replaceLineEdit.setFixedWidth(200)
        self.replaceLineEdit.setFixedHeight(30)
        self.replaceLineEdit.setFont(QFont('SansSerif', 14))
        self.replaceLineEdit.setStyleSheet("color: rgb(255, 255, 255);")
        self.ui.toolBar.insertWidget(self.ui.actionReplace, self.replaceLineEdit)

        self.GotoLineEdit = QLineEdit(self)
        self.GotoLineEdit.setFixedWidth(100)
        self.GotoLineEdit.setFixedHeight(30)
        self.GotoLineEdit.setFont(QFont('SansSerif', 14))
        self.GotoLineEdit.setStyleSheet("color: rgb(255, 255, 255);")
        self.ui.toolBar.insertWidget(self.ui.actionGogo, self.GotoLineEdit)



        self.ui.dockWidget_message.setFloating(False)
        self.ui.tabWidget.setTabsClosable(True)
        self.ui.tabWidget.removeTab(0)
        self.ui.tabWidget.removeTab(0)
        self.tabCount = 2
        self.ui.tabWidget.tabCloseRequested.connect(self.closeTab)
        self.editor = SimplePythonEditor()
        self.ui.tabWidget.addTab(self.editor, 'New File 1')
            #### File Menu all action
        self.ui.actionNew.triggered.connect(self.newfile_action)
        self.ui.actionOpen.triggered.connect(self.openfile_action)
        self.ui.actionOpen_Folder.triggered.connect(self.open_folder_action)
        self.ui.actionSave_File.triggered.connect(self.savefile_actoin)
        self.ui.actionSave_As.triggered.connect(self.save_as_action)
        self.ui.actionClose_File.triggered.connect(self.closeTab)
        self.ui.actionExit.triggered.connect(self.exit_action)
            ##### Edit mune All Action #####
        self.ui.actionCut.triggered.connect(self.cut_action)
        self.ui.actionCopy.triggered.connect(self.copy_action)
        self.ui.actionPaste.triggered.connect(self.paste_action)
        self.ui.actionSelect_All.triggered.connect(self.select_all_action)
        self.ui.actionUndo.triggered.connect(self.undo_action)
        self.ui.actionRedo.triggered.connect(self.redo_action)
        self.ui.actionFind.triggered.connect(self.find_actio)
        self.ui.actionReplace.triggered.connect(self.replace_action)
        self.ui.actionGogo.triggered.connect(self.goto_action)
                ##### View Mune All Action
        self.ui.actionMessage_Window.triggered.connect(self.message_window_action)
        self.ui.actiontool_Window.triggered.connect(self.tool_box_action)
        self.ui.actionProject_Windows.triggered.connect(self.project_window_action)
        self.ui.actionProparty_Window.triggered.connect(self.property_window_action)
                    ##### Run Mune All Action
        self.ui.actionCompile.triggered.connect(self.compile_action)
        self.ui.actionRun.triggered.connect(self.run_action)
        self.ui.actionCompile_And_Run.triggered.connect(self.compile_and_run_action)
                    ###### Debug Mune All Action
        self.ui.actionStart_Debug.triggered.connect(self.start_debug_action)
        self.ui.actionExecute_Next_Line.triggered.connect(self.execute_next_line_action)
        self.ui.actionExecute_Next_Function.triggered.connect(self.execute_next_funtion_action)
        self.ui.actionGoto_Next_Breakpoint.triggered.connect(self.goto_next_breackpoint_action)
        self.ui.actionEnd_Debug.triggered.connect(self.end_debug_action)
        self.ui.actionBreakpoint.triggered.connect(self.breackpoint_action)
        self.ui.actionWatch.triggered.connect(self.watch_action)
        self.ui.actionTerminal_Window.triggered.connect(self.showTerminal_Window)

        self.ui.actionSimple_Python_Project.triggered.connect(self.Simple_Python_Project)
        self.ui.actionQT_GUI_Application.triggered.connect(self.QT_GUI_Application)



        self.ui.dockWidget_tools.setVisible(False)
        self.ui.dockWidget_project.setVisible(True)
        self.ui.dockWidget_preproty.setVisible(False)
        self.erronOnCompial=False
        self.ui.treeView.doubleClicked.connect(self.treeViewopenFile)
        self.conn = sqlite3.connect('database.db')
        print("Opened database successfully")
        cursor = self.conn.execute("SELECT fileName from openFiles group by fileName")
        for row in cursor:
            try:
                print(" file name ="+str(row[0]))
                ne = SimplePythonEditor()
                fileTital = ne.openFile_form_command_line(str(row[0]))
                tfileName = fileTital
                tfileName = tfileName.split('/')
                fileName = tfileName[len(tfileName) - 1]
                self.ui.tabWidget.addTab(ne, fileName)
                self.tabCount = self.tabCount + 1
                self.ui.tabWidget.setCurrentIndex(self.ui.tabWidget.count() - 1)
            except:
                pass
        cursor = self.conn.execute("SELECT folderPath from openFolder order by id desc")
        for row in cursor:
            folder = str(row[0])
            if folder:
                self.currentFolder=folder
                print(folder)
                self.model = QFileSystemModel()
                self.model.setRootPath((QtCore.QDir.rootPath()))
                self.ui.treeView.setModel(self.model)
                self.ui.treeView.setRootIndex(self.model.index(folder))
                self.ui.treeView.setSortingEnabled(True)
                self.ui.treeView.setColumnWidth(0, 800)
                self.conn.execute("insert into openFolder values(null,'" + folder + "')")
                self.conn.commit()
                break

    def QT_GUI_Application(self):
        dlg = cls_pyqtProject()
        if dlg.exec_():
            destination_dir = dlg.pLocation + dlg.pName
            if not os.path.exists(destination_dir):
                os.makedirs(destination_dir)

            uifileName = destination_dir + "\\" + dlg.uifileName
            pyfileName = destination_dir + "\\" + dlg.pyfileName
            classfileName = destination_dir + "\\" + dlg.classfileName

            u = open(uifileName, "w")
            fileData = ""
            fileData = fileData + "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" + "\n"
            fileData = fileData + "<ui version=\"4.0\">" + "\n"
            fileData = fileData + " <class>MainWindow</class>" + "\n"
            fileData = fileData + " <widget class=\"QMainWindow\" name=\"MainWindow\">" + "\n"
            fileData = fileData + "  <property name=\"geometry\">" + "\n"
            fileData = fileData + "   <rect>" + "\n"
            fileData = fileData + "    <x>0</x>" + "\n"
            fileData = fileData + "    <y>0</y>" + "\n"
            fileData = fileData + "    <width>800</width>" + "\n"
            fileData = fileData + "    <height>600</height>" + "\n"
            fileData = fileData + "   </rect>" + "\n"
            fileData = fileData + "  </property>" + "\n"
            fileData = fileData + "  <property name=\"windowTitle\">" + "\n"
            fileData = fileData + "   <string>MainWindow</string>" + "\n"
            fileData = fileData + "  </property>" + "\n"
            fileData = fileData + "  <widget class=\"QWidget\" name=\"centralwidget\"/>" + "\n"
            fileData = fileData + "  <widget class=\"QMenuBar\" name=\"menubar\">" + "\n"
            fileData = fileData + "   <property name=\"geometry\">" + "\n"
            fileData = fileData + "    <rect>" + "\n"
            fileData = fileData + "     <x>0</x>" + "\n"
            fileData = fileData + "     <y>0</y>" + "\n"
            fileData = fileData + "     <width>800</width>" + "\n"
            fileData = fileData + "     <height>21</height>" + "\n"
            fileData = fileData + "    </rect>" + "\n"
            fileData = fileData + "   </property>" + "\n"
            fileData = fileData + "  </widget>" + "\n"
            fileData = fileData + "  <widget class=\"QStatusBar\" name=\"statusbar\"/>" + "\n"
            fileData = fileData + " </widget>" + "\n"
            fileData = fileData + " <resources/>" + "\n"
            fileData = fileData + " <connections/>" + "\n"
            fileData = fileData + "</ui>" + "\n"
            u.write(fileData)
            u.close()

            p = open(pyfileName, "w")
            fileData = ""
            fileData = fileData + "# -*- coding: utf-8 -*-" + "\n"
            fileData = fileData + "#" + "\n"
            fileData = fileData + "# Created by: PyQt5 UI code generator 5.15.7" + "\n"
            fileData = fileData + "#" + "\n"
            fileData = fileData + "# WARNING: Any manual changes made to this file will be lost when pyuic5 is" + "\n"
            fileData = fileData + "# run again.  Do not edit this file unless you know what you are doing." + "\n"

            fileData = fileData + "from PyQt5 import QtCore, QtGui, QtWidgets" + "\n"

            fileData = fileData + "class Ui_MainWindow(object):" + "\n"
            fileData = fileData + "    def setupUi(self, MainWindow):" + "\n"
            fileData = fileData + "        MainWindow.setObjectName(\"MainWindow\")" + "\n"
            fileData = fileData + "        MainWindow.resize(800, 600)" + "\n"
            fileData = fileData + "        self.centralwidget = QtWidgets.QWidget(MainWindow)" + "\n"
            fileData = fileData + "        self.centralwidget.setObjectName(\"centralwidget\")" + "\n"
            fileData = fileData + "        MainWindow.setCentralWidget(self.centralwidget)" + "\n"
            fileData = fileData + "        self.menubar = QtWidgets.QMenuBar(MainWindow)" + "\n"
            fileData = fileData + "        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))" + "\n"
            fileData = fileData + "        self.menubar.setObjectName(\"menubar\")" + "\n"
            fileData = fileData + "        MainWindow.setMenuBar(self.menubar)" + "\n"
            fileData = fileData + "        self.statusbar = QtWidgets.QStatusBar(MainWindow)" + "\n"
            fileData = fileData + "        self.statusbar.setObjectName(\"statusbar\")" + "\n"
            fileData = fileData + "        MainWindow.setStatusBar(self.statusbar)" + "\n"
            fileData = fileData + "        self.retranslateUi(MainWindow)" + "\n"
            fileData = fileData + "        QtCore.QMetaObject.connectSlotsByName(MainWindow)" + "\n"
            fileData = fileData + "    def retranslateUi(self, MainWindow):" + "\n"
            fileData = fileData + "        _translate = QtCore.QCoreApplication.translate" + "\n"
            fileData = fileData + "        MainWindow.setWindowTitle(_translate(\"MainWindow\", \"MainWindow\"))" + "\n"
            p.write(fileData)
            p.close()

            ff = str(dlg.pyfileName).split('.')
            c = open(classfileName, "w")
            fileData = ""
            fileData = fileData + "from PyQt5 import QtCore, QtGui, QtWidgets" + "\n"
            fileData = fileData + "from "+ff[0]+" import Ui_MainWindow" + "\n"
            fileData = fileData + "class "+ff[0]+"(QtWidgets.QMainWindow):" + "\n"
            fileData = fileData + "    def __init__(self):" + "\n"
            fileData = fileData + "        super("+ff[0]+", self).__init__()" + "\n"
            fileData = fileData + "        self.ui = Ui_MainWindow()" + "\n"
            fileData = fileData + "        self.ui.setupUi(self)" + "\n"

            c.write(fileData)
            c.close()

            ff=str(dlg.pyfileName).split('.')
            cc=str(dlg.classfileName).split('.')
            mainFileName = destination_dir + "\\" + dlg.pName + ".py"
            f = open(mainFileName, "w")
            fileData = ""
            fileData = fileData + "from PyQt5 import QtCore, QtGui, QtWidgets" + "\n"
            fileData = fileData + "from "+cc[0]+" import "+ff[0] + "\n"
            fileData = fileData + "import sys" + "\n"
            fileData = fileData + "software = QtWidgets.QApplication([])" + "\n"
            fileData = fileData + "main_from = "+ff[0]+"()" + "\n"
            fileData = fileData + "main_from.show()" + "\n"
            fileData = fileData + "sys.exit(software.exec())" + "\n"
            f.write(fileData)
            f.close()
            ne = SimplePythonEditor()
            fileTital = ne.openFile_form_command_line(str(mainFileName))
            tfileName = fileTital
            tfileName = tfileName.split('/')
            fileName = tfileName[len(tfileName) - 1]
            self.ui.tabWidget.addTab(ne, fileName)
            self.tabCount = self.tabCount + 1
            self.ui.tabWidget.setCurrentIndex(self.ui.tabWidget.count() - 1)
            self.conn.execute("insert into openFiles values(null,'" + mainFileName + "')")
            self.conn.commit()

            self.conn.execute("insert into openFolder values(null,'" + destination_dir + "')")
            self.conn.commit()

            folder = destination_dir
            self.currentFolder=destination_dir
            if folder:
                print(folder)
                self.model = QFileSystemModel()
                self.model.setRootPath((QtCore.QDir.rootPath()))
                self.ui.treeView.setModel(self.model)
                self.ui.treeView.setRootIndex(self.model.index(folder))
                self.ui.treeView.setSortingEnabled(True)
                self.ui.treeView.setColumnWidth(0, 800)
                self.conn.execute("insert into openFolder values(null,'" + destination_dir + "')")
                self.conn.commit()

        else:
            print("Click on cancle Button")

    def Simple_Python_Project(self):
        dlg = cls_SimplePythonProject()
        if dlg.exec_():
            print("Click on Ok Button ")
            print(str(dlg.pName))
            print(str(dlg.pLocation))
            destination_dir=dlg.pLocation+"\\"+dlg.pName
            if not os.path.exists(destination_dir):
                os.makedirs(destination_dir)
            mainFileName=destination_dir+"\\"+dlg.pName+".py"
            f = open(mainFileName, "w")
            fileData="";
            fileData = fileData + "def print_hi(name):" + "\n"
            fileData = fileData + "\tprint(f'Hi, {name}') " + "\n"
            fileData = fileData + "" + "\n"
            fileData = fileData + "if __name__ == '__main__':" + "\n"
            fileData = fileData + "\tprint_hi('PyCharm')" + "\n"
            f.write(fileData)
            f.close()
            ne = SimplePythonEditor()
            fileTital = ne.openFile_form_command_line(str(mainFileName))
            tfileName = fileTital
            tfileName = tfileName.split('/')
            fileName = tfileName[len(tfileName) - 1]
            self.ui.tabWidget.addTab(ne, fileName)
            self.tabCount = self.tabCount + 1
            self.ui.tabWidget.setCurrentIndex(self.ui.tabWidget.count() - 1)
            self.conn.execute("insert into openFiles values(null,'" + mainFileName + "')")
            self.conn.commit()

            self.conn.execute("insert into openFolder values(null,'" + destination_dir + "')")
            self.conn.commit()

            folder = destination_dir
            if folder:
                print(folder)
                self.model = QFileSystemModel()
                self.model.setRootPath((QtCore.QDir.rootPath()))
                self.ui.treeView.setModel(self.model)
                self.ui.treeView.setRootIndex(self.model.index(folder))
                self.ui.treeView.setSortingEnabled(True)
                self.ui.treeView.setColumnWidth(0, 800)
                self.conn.execute("insert into openFolder values(null,'" + destination_dir + "')")
                self.conn.commit()

        else:
            print("Click on cancle Button")

    def showTerminal_Window(self):
        os.system("start /B start cmd.exe @cmd /k cd C:\\Users\\ap\\AppData\\Local\\Programs\\Python\\Python38\\")

    def treeViewopenFile(self):

        #file = [r'C:\Program Files (x86)\Qt Designer\designer.exe', 'C:\\Users\\ap\\Documents\\K4\\form1.ui']
        #subprocess.call(file)

        index = self.ui.treeView.currentIndex()
        file_path = self.model.filePath(index)
        ff=file_path.split('.')
        ext=ff[len(ff) - 1]
        if ext=="ui":
            pass
            file = [r'C:\Program Files (x86)\Qt Designer\designer.exe', file_path ]
            subprocess.call(file)
        else:
            print(file_path)
            #os.startfile(file_path)
            ne = SimplePythonEditor()

            fileName = file_path
            fullFileName = file_path
            status = 0
            for i in range(0, self.ui.tabWidget.count()):
                xx = self.ui.tabWidget.widget(i)
                if fullFileName == xx.getFullFileName():
                    status = 1
                    break
            if status == 1:
                self.ui.tabWidget.setCurrentIndex(i)
            else:
                fileTital = ne.openFile_form_command_line(fileName)
                tfileName = fileTital
                tfileName = tfileName.split('/')
                fileName = tfileName[len(tfileName) - 1]
                self.ui.tabWidget.addTab(ne, fileName)
                self.tabCount = self.tabCount + 1
                self.ui.tabWidget.setCurrentIndex(self.ui.tabWidget.count() - 1)

    def closeTab (self, currentIndex):
        xx = self.ui.tabWidget.widget(currentIndex)
        ff=xx.getFullFileName()
        self.conn.execute("delete from  openFiles  where fileName='"+ff+"'")
        self.conn.commit()
        self.ui.tabWidget.removeTab(currentIndex)
        self.tabCount = self.tabCount - 1
        if currentIndex == 0 and self.tabCount==-1 :
            self.editor.setText("")
            self.ui.tabWidget.addTab(self.editor, 'New File')
            self.tabCount = self.tabCount + 1

    def changeTitalofActiveTab(self,tital):
        self.ui.tabWidget.setWindowTitle("dsfsdfdsfds")
        self.ui.tabWidget.setTabText(self.ui.tabWidget.currentIndex(),tital)

    def newfile_action(self):
        tfileName='New File'+str(self.tabCount)
        self.editor = SimplePythonEditor()
        self.editor.setText("")
        self.editor.setFullFileNmae(tfileName)
        self.ui.tabWidget.addTab(self.editor, tfileName)
        self.tabCount = self.tabCount + 1

    def getActiveTabIndex(self):
        yy = self.ui.tabWidget.currentWidget()
        for i in range(0,self.ui.tabWidget.count()):
            xx = self.ui.tabWidget.widget(i)
            if yy.getFullFileName() == xx.getFullFileName():
                break
        print(i)
        return i
    def openfile_action(self):
        ne = SimplePythonEditor()

        fileName = QFileDialog.getOpenFileName()
        fullFileName = fileName[0]
        status=0
        for i in range(0, self.ui.tabWidget.count()):
            xx = self.ui.tabWidget.widget(i)
            if fullFileName == xx.getFullFileName():
                status = 1
                break
        if status == 1:
            self.ui.tabWidget.setCurrentIndex(i)
        else:
            fileTital= ne.openFile(fileName)
            tfileName = fileTital
            tfileName = tfileName.split('/')
            fileName = tfileName[len(tfileName) - 1]
            self.ui.tabWidget.addTab(ne, fileName)
            self.tabCount = self.tabCount + 1
            self.ui.tabWidget.setCurrentIndex(self.ui.tabWidget.count()-1)
            self.conn.execute("insert into openFiles values(null,'"+fileTital+"')")
            self.conn.commit()
    def openfile_form_command_line_action(self,fileName):
        print(fileName)
        #self.closeTab(0)
        ne = SimplePythonEditor()
        fileTital = ne.openFile_form_command_line(fileName)
        tfileName = fileTital
        tfileName = tfileName.split('/')
        fileName = tfileName[len(tfileName) - 1]
        self.ui.tabWidget.addTab(ne, fileName)
        self.tabCount = self.tabCount + 1
        self.ui.tabWidget.setCurrentIndex(self.ui.tabWidget.count() - 1)
        self.conn.execute("insert into openFiles values(null,'" + fileTital + "')")
        self.conn.commit()

    def open_folder_action(self):
        folder = QFileDialog.getExistingDirectory(self, 'Project Data', '')
        if folder:
            print(folder)
            self.model = QFileSystemModel()
            self.model.setRootPath((QtCore.QDir.rootPath()))
            self.ui.treeView.setModel(self.model)
            self.ui.treeView.setRootIndex(self.model.index(folder))
            self.ui.treeView.setSortingEnabled(True)
            self.ui.treeView.setColumnWidth(0, 800)
            self.conn.execute("insert into openFolder values(null,'" + folder + "')")
            self.conn.commit()
    def savefile_actoin(self):
        i = self.getActiveTabIndex()
        xx = self.ui.tabWidget.widget(i)
        status = xx.getSaveStatus()
        if status == "Yes":
            ff=xx.getFullFileName()
            try:
                f = open(xx.getFullFileName(), "w")
                f.write(xx.text())
                f.close()
                self.conn.execute("insert into openFiles values(null,'" + ff + "')")
                self.conn.commit()
            except Exception as e:
                print(e)
        else:
            try:
                fileName = QFileDialog.getSaveFileName()
                xx.saveFile(fileName)
                tfileName = fileName[0].split('/')
                fileName = tfileName[len(tfileName) - 1]
                self.ui.tabWidget.setTabText(self.getActiveTabIndex(), fileName)
            except Exception as e:
                print(e)

    def save_as_action(self):
        i = self.getActiveTabIndex()
        xx = self.ui.tabWidget.widget(i)
        fileName = QFileDialog.getSaveFileName()
        xx.saveFile(fileName)
        tfileName = fileName[0].split('/')
        fileName = tfileName[len(tfileName) - 1]
        self.ui.tabWidget.setTabText(self.getActiveTabIndex(), fileName)

    def exit_action(self):
        sys.exit()

        ###Edit Mune All Action
    def cut_action(self):
        i = self.getActiveTabIndex()
        xx = self.ui.tabWidget.widget(i)
        xx.cut()

    def copy_action(self):
        i = self.getActiveTabIndex()
        xx = self.ui.tabWidget.widget(i)
        xx.copy()

    def paste_action(self):
        i = self.getActiveTabIndex()
        xx = self.ui.tabWidget.widget(i)
        xx.paste()

    def select_all_action(self):
        i = self.getActiveTabIndex()
        xx = self.ui.tabWidget.widget(i)
        xx.selectAll()
    def undo_action(self):
        i = self.getActiveTabIndex()
        xx = self.ui.tabWidget.widget(i)
        xx.undo()
    def redo_action(self):
        i = self.getActiveTabIndex()
        xx = self.ui.tabWidget.widget(i)
        xx.redo()

    def find_actio(self):
        i = self.getActiveTabIndex()
        xx = self.ui.tabWidget.widget(i)
        textToFind= self.findLineEdit.text()
        if textToFind=="":
            self.findLineEdit.setFocus()
        else:
            SaveStatus = xx.findFunction(textToFind,True)



    def replace_action(self):
        i = self.getActiveTabIndex()
        xx = self.ui.tabWidget.widget(i)
        text= str(xx.text())
        textToFind = self.findLineEdit.text()
        textToreplace = self.replaceLineEdit.text()
        ln, ps = xx.getCursorPosition()
        if textToFind == "":
            self.findLineEdit.setFocus()
        else:
            if textToreplace== "":
                self.replaceLineEdit.setFocus()
            else:
                xx.setText(text.replace(textToFind,textToreplace))
                xx.ensureLineVisible(ln)
                xx.setCursorPosition(ln, ps)

    def goto_action(self):
        i = self.getActiveTabIndex()
        xx = self.ui.tabWidget.widget(i)
        lineNumber= int(self.GotoLineEdit.text())
        xx.ensureLineVisible(lineNumber)
        xx.setCursorPosition(lineNumber, 1)
        #xx.Lines[50 - 1].Goto()


        ##### View Mune All Action
    def message_window_action(self):
            if self.message_window_status==True:
                self.ui.dockWidget_message.setVisible(False)
                self.message_window_status = False
                self.ui.actionMessage_Window.setIconVisibleInMenu(False)
            else:
                self.ui.dockWidget_message.setVisible(True)
                self.message_window_status = True
                self.ui.actionMessage_Window.setIconVisibleInMenu(True)

    def tool_box_action(self):
        pass
        # if self.tool_box_status == True:
        #     self.ui.dockWidget_tools.setVisible(False)
        #     self.tool_box_status = False
        #     self.ui.actiontool_Window.setIconVisibleInMenu(False)
        # else:
        #     self.ui.dockWidget_tools.setVisible(True)
        #     self.tool_box_status = True
        #     self.ui.actiontool_Window.setIconVisibleInMenu(True)

    def project_window_action(self):
         if self.project_window_status == True:
             self.ui.dockWidget_project.setVisible(False)
             self.project_window_status =False
             self.ui.actionProject_Windows.setIconVisibleInMenu(False)
         else:
             self.ui.dockWidget_project.setVisible(True)
             self.project_window_status = True
             self.ui.actionProject_Windows.setIconVisibleInMenu(True)

    def property_window_action(self):
        pass
        # if self.project_window_status == True:
        #     self.ui.dockWidget_preproty.setVisible(False)
        #     self.property_window_status = False
        #     self.ui.actionProparty_Window.setIconVisibleInMenu(False)
        # else:
        #     self.ui.dockWidget_preproty.setVisible(True)
        #     self.property_window_status = True
        #     self.ui.actionProparty_Window.setIconVisibleInMenu(True)

        ##### Run Mune All Action
    def compile_action(self):
        txtfiles = []
        aaa=self.currentFolder+"\\*.ui"
        for file in glob.glob(aaa):
            txtfiles.append(file)
            uifile = txtfiles
            py = txtfiles[0].split(".")
            print("pyuic5 "+txtfiles[0]+" -o "+py[0]+".py")
            outputFile=py[0]+"_code.py"
             print(outputFile)
            try :
                subprocess.call([r"C:\Users\vinit\AppData\Local\Programs\Python\Python38\python.exe", "pyuic5", uifile, "-o", outputFile])
            except Exception as e:
                print(e)






    def run_action(self):
        i = self.getActiveTabIndex()
        xx = self.ui.tabWidget.widget(i)
        SaveStatus = xx.getSaveStatus()
        if SaveStatus == "Yes":
            xfn = xx.getFullFileName()
            print("xfn is" + xfn)
            extentions = xfn.split('.')
            extention = extentions[len(extentions) - 1]
            if extention == 'py':
                #os.environ["python"] = r"C:\Users\vinit\AppData\Local\Programs\Python\Python38\python.exe"
                #p = Popen(['python',  xfn, ], )
                appDataPath = os.getenv('APPDATA')
                CCpath = os.path.join(appDataPath, "Ezapiya")
                data_for_batch_file = "@ECHO OFF \n"
                data_for_batch_file = data_for_batch_file + "python " + xfn + "\n"
                data_for_batch_file = data_for_batch_file + "\nstop_.exe"
                batFileName = CCpath + "\\run.bat"
                f = open(batFileName, "w")
                f.write(data_for_batch_file)
                f.close()
                p = subprocess.Popen(batFileName, creationflags=subprocess.CREATE_NEW_CONSOLE)
        if SaveStatus == "No":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("File is Not Save. Do you want to save this file")
            msg.setWindowTitle("Ezapiya IDE")
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            # msg.buttonClicked.connect(self.msgbtn)
            retval = msg.exec_()
            if retval == QMessageBox.Yes:
                self.savefile_actoin()


    def compile_and_run_action(self):
        self.erronOnCompial = True
        i = self.getActiveTabIndex()
        xx = self.ui.tabWidget.widget(i)
        SaveStatus = xx.getSaveStatus()
        if SaveStatus == "Yes":
            xfn = xx.getFullFileName()
            print("xfn is" + xfn)
            extentions = xfn.split('.')
            extention = extentions[len(extentions) - 1]
            if extention == 'py':
                #os.environ["python"] = r"C:\Users\vinit\AppData\Local\Programs\Python\Python38\python.exe"
                #p = Popen(['python',  xfn, ], )
                appDataPath = os.getenv('APPDATA')
                CCpath = os.path.join(appDataPath, "Ezapiya")
                data_for_batch_file = "@ECHO OFF \n"
                data_for_batch_file = data_for_batch_file + "python " + xfn + "\n"
                data_for_batch_file = data_for_batch_file + "\nstop_.exe"
                batFileName = CCpath + "\\run.bat"
                f = open(batFileName, "w")
                f.write(data_for_batch_file)
                f.close()
                p = subprocess.Popen(batFileName, creationflags=subprocess.CREATE_NEW_CONSOLE)

        if SaveStatus == "No":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("File is Not Save. Do you want to save this file")
            msg.setWindowTitle("Ezapiya IDE")
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            # msg.buttonClicked.connect(self.msgbtn)
            retval = msg.exec_()
            if retval == QMessageBox.Yes:
                self.savefile_actoin()

    ###### Debug Mune All Action


    def start_debug_action(self):
        print("start")

    def execute_next_line_action(self):
        print("line")
    def execute_next_funtion_action(self):
        print("funtion")
    def goto_next_breackpoint_action(self):
        print("goto")
    def end_debug_action(self):
        print("end")
    def breackpoint_action(self):
        print("breack")
    def watch_action(self):
        print("watch")

    def load_project_structure(sefl,startpath, tree):
        """
        Load Project structure tree
        :param startpath:
        :param tree:
        :return:
        """
        import os
        from PyQt5.QtWidgets import QTreeWidgetItem
        from PyQt5.QtGui import QIcon
        for element in os.listdir(startpath):
            path_info = startpath + "/" + element
            parent_itm = QTreeWidgetItem(tree, [os.path.basename(element)])
            if os.path.isdir(path_info):
                sefl.load_project_structure(path_info, parent_itm)
                parent_itm.setIcon(0, QIcon('assets/folder.ico'))
            else:
                parent_itm.setIcon(0, QIcon('assets/file.ico'))