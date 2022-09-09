from PyQt5 import Qsci
from PyQt5.QtGui import *
from PyQt5.Qsci import QsciScintilla, QsciLexerPython, QsciLexerCPP, QsciLexerJava, QsciLexerJavaScript, \
    QsciLexerCSharp, QsciLexerHTML, QsciLexerCSS, QsciLexerXML, QsciLexerSQL
from PyQt5.QtWidgets import QApplication, QShortcut, QFileDialog
import keyword
class SimplePythonEditor(QsciScintilla):
    ARROW_MARKER_NUM = 8
    def __init__(self, parent=None):
        super(SimplePythonEditor, self).__init__(parent)
        self.fullFileName = ""
        self.fileName = ""
        self.fileExtention = ""
        self.saveStatus = "No"
        self.TabID=0

        font = QFont()
        font.setFamily('Courier')
        font.setFixedPitch(True)
        font.setPointSize(16)
        self.setFont(font)
        self.setMarginsFont(font)
        self.setPaper(QColor('lightblue'))
        fontmetrics = QFontMetrics(font)
        self.setMarginsFont(font)
        self.setMarginWidth(0, fontmetrics.width("00000") + 6)
        self.setMarginLineNumbers(0, True)
        self.setMarginsBackgroundColor(QColor("#232323"))
        self.setMarginsForegroundColor(QColor("#FFF"))
        self.setMarginSensitivity(1, True)
        self.markerDefine(QsciScintilla.RightArrow, self.ARROW_MARKER_NUM)
        self.setMarkerBackgroundColor(QColor("#ee1111"), self.ARROW_MARKER_NUM)
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)
        self.setCaretLineBackgroundColor(QColor("#264026"))
        self.setCaretForegroundColor(QColor("#000000"))
        self.setCaretLineVisible(True)
        lexer = QsciLexerPython()

        lexer.setDefaultFont(QFont("Consolas", 14))
        lexer.setDefaultPaper(QColor("#3c3c3c"))
        lexer.setDefaultColor(QColor("#f9f9f9"))

        lexer.setFont(QFont("Consolas", 14), 0)
        lexer.setFont(QFont("Consolas", 14), 1)
        lexer.setFont(QFont("Consolas", 14), 2)
        lexer.setFont(QFont("Consolas", 14), 3)
        lexer.setFont(QFont("Consolas", 14), 4)
        lexer.setFont(QFont("Consolas", 14), 5)
        lexer.setFont(QFont("Consolas", 14), 6)
        lexer.setFont(QFont("Consolas", 14), 7)
        lexer.setFont(QFont("Consolas", 14), 8)
        lexer.setFont(QFont("Consolas", 14), 9)
        lexer.setFont(QFont("Consolas", 14), 10)
        lexer.setFont(QFont("Consolas", 14), 11)
        lexer.setFont(QFont("Consolas", 14), 12)
        lexer.setFont(QFont("Consolas", 14), 13)
        lexer.setFont(QFont("Consolas", 14), 14)
        lexer.setFont(QFont("Consolas", 14), 15)

        lexer.setColor(QColor("#FFF"), 0)  # Default = 0
        lexer.setColor(QColor("#05FE40"), 1)  # Comment = 1
        lexer.setColor(QColor("#FFF"), 2)  # Number = 2#
        lexer.setColor(QColor("#E7DB74"), 3)  # DoubleQuotedString = 3#
        lexer.setColor(QColor("#B36932"), 4)  # SingleQuotedString = 4#
        lexer.setColor(QColor("#FEFB02"), 5)  # Keyword = 5#
        lexer.setColor(QColor("#E7DB74"), 6)  # TripleSingleQuotedString = 6#
        lexer.setColor(QColor("#E7DB74"), 7)  # TripleDoubleQuotedString = 7#
        lexer.setColor(QColor("#88E22B"), 8)  # ClassName = 8#
        lexer.setColor(QColor("#FDD68A"), 9)  # FunctionMethodName = 9#
        lexer.setColor(QColor("#EC5166"), 10)  # Operator = 10#
        lexer.setColor(QColor("#60D8EF"), 11)  # Identifier = 11#
        lexer.setColor(QColor("#C5A84F"), 12)  # CommentBlock = 12
        lexer.setColor(QColor("#B9644F"), 13)  # UnclosedString = 13
        lexer.setColor(QColor("#C3485C"), 14)  # HighlightedIdentifier = 14
        lexer.setColor(QColor("#498B60"), 15)  # Decorator = 15

        self.setCaretForegroundColor(QColor("#000000"))
        self.setCaretWidth(5)
        self.setTabWidth(4)
        self.setIndentationGuides(True)
        self.setTabIndents(True)
        self.setAutoIndent(True)
        self.setFolding(QsciScintilla.BoxedTreeFoldStyle)
        my_list = [".", " ", "{", "}", "[", "]", "(", ")", ":", ";"]
        self.setAutoCompletionWordSeparators(my_list)
        self.setLexer(lexer)
        api = Qsci.QsciAPIs(lexer)
        for key in keyword.kwlist + dir(__builtins__):
            api.add(key)
        api.add("aLongString")
        api.add("aLongerString")
        api.add("aDifferentString")
        api.add("sOmethingElse")
        api.prepare()
        self.setAutoCompletionCaseSensitivity(False)
        self.setAutoCompletionReplaceWord(False)
        self.setAutoCompletionThreshold(1)
        self.setAutoCompletionSource(Qsci.QsciScintilla.AcsAll)
        self.SendScintilla(QsciScintilla.SCI_SETHSCROLLBAR, 0)
        shortcut_ctrl_space = QShortcut(QKeySequence("Ctrl+Space"), self);

        # self.connect(shortcut_ctrl_space, SIGNAL(activated()), self,SLOT(autoCompleteFromAll()));

    def on_margin_clicked(self, nmargin, nline, modifiers):
        if self.markersAtLine(nline) != 0:
            self.markerDelete(nline, self.ARROW_MARKER_NUM)
        else:
            self.markerAdd(nline, self.ARROW_MARKER_NUM)

    def findFunction(self,wordToFind,forward):
        if forward:
            line, index = self.getSelection()[2:]
        else:
            line, index = self.getSelection()[:2]

        self.findFirst(wordToFind, False, False, False, False, True, line, index, False)


    def openFile(self,fileName):
        self.fullFileName = fileName[0]
        tfileName=fileName[0]
        tfileName=tfileName.split('/')
        self.fileName = tfileName[len(tfileName)-1]
        ext = self.fileName.split('.')
        self.fileExtention = ext[len(ext)-1]
        f = open(self.fullFileName,"r")
        self.setText(f.read())
        f.close()
        self.saveStatus = "Yes"

        if self.fileExtention=="c" or self.fileExtention=="cpp" :
            self.setCpplexer()
        if self.fileExtention=="py":
            self.setPythonlexer()
        if self.fileExtention == "java":
            self.setJavalexer()
        if self.fileExtention == "js":
            self.setJavaScriptlexer()
        if self.fileExtention == "cs":
            self.setCSharplexer()
        if self.fileExtention == "html" or self.fileExtention == "htm":
            self.setHtmllexe()

        if self.fileExtention == "sql":
            self.setSQLlexe()
        if self.fileExtention == "xml":
            self.setXMLlexe()
        if self.fileExtention == "css":
            self.setCSSlexe()

        return self.fullFileName

    def openFile_form_command_line(self,fileName):
        self.fullFileName = fileName
        tfileName=fileName
        tfileName=tfileName.split('/')
        self.fileName = tfileName[len(tfileName)-1]
        ext = self.fileName.split('.')
        self.fileExtention = ext[len(ext)-1]
        f = open(self.fullFileName,"r")
        self.setText(f.read())
        f.close()
        self.saveStatus = "Yes"

        if self.fileExtention=="c" or self.fileExtention=="cpp" :
            self.setCpplexer()
        if self.fileExtention=="py":
            self.setPythonlexer()
        if self.fileExtention == "java":
            self.setJavalexer()
        if self.fileExtention == "js":
            self.setJavaScriptlexer()
        if self.fileExtention == "cs":
            self.setCSharplexer()
        if self.fileExtention == "html" or self.fileExtention == "htm":
            self.setHtmllexe()

        if self.fileExtention == "sql":
            self.setSQLlexe()
        if self.fileExtention == "xml":
            self.setXMLlexe()
        if self.fileExtention == "css":
            self.setCSSlexe()

        return self.fullFileName

    def getSaveStatus(self):
        return self.saveStatus

    def saveFile(self, fileName):
        self.fullFileName = fileName[0]
        tfileName = fileName[0]
        tfileName = tfileName.split('/')
        self.fileName = tfileName[len(tfileName) - 1]
        print(self.fileName)
        ext = self.fileName.split('.')
        self.fileExtention = ext[len(ext) - 1]
        f = open(self.fullFileName, "w")
        f.write(self.text())
        f.close()
        self.saveStatus = "Yes"

        if self.fileExtention == "c" or self.fileExtention == "cpp":
            self.setCpplexer()
        if self.fileExtention == "py":
            self.setPythonlexer()
        if self.fileExtention == "java":
            self.setJavalexer()
        if self.fileExtention == "js":
            self.setJavaScriptlexer()
        if self.fileExtention == "cs":
            self.setCSharplexer()
        if self.fileExtention == "html" or self.fileExtention == "htm":
            self.setHtmllexe()
        if self.fileExtention == "css":
            self.setXMLlexe()
        if self.fileExtention == "sql":
            self.setSQLlexe()
        if self.fileExtention == "sql":
            self.setSQLlexe()
        if self.fileExtention == "xml":
            self.setXMLlexe()
        if self.fileExtention == "css":
            self.setCSSlexe()


    def getFullFileName(self):
        return self.fullFileName

    def setCommand(self, Command):
        pass
    def setFullFileNmae(self, Fname):
        self.fullFileName = Fname


    def setPythonlexer(self):
        font = QFont()
        font.setFamily('Courier')
        font.setFixedPitch(True)
        font.setPointSize(16)
        self.setFont(font)
        self.setMarginsFont(font)
        self.setPaper(QColor('lightblue'))
        fontmetrics = QFontMetrics(font)
        self.setMarginsFont(font)
        self.setMarginWidth(0, fontmetrics.width("00000") + 6)
        self.setMarginLineNumbers(0, True)
        self.setMarginsBackgroundColor(QColor("#232323"))
        self.setMarginsForegroundColor(QColor("#FFF"))
        self.setMarginSensitivity(1, True)
        self.markerDefine(QsciScintilla.RightArrow, self.ARROW_MARKER_NUM)
        self.setMarkerBackgroundColor(QColor("#ee1111"), self.ARROW_MARKER_NUM)
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)
        self.setCaretLineBackgroundColor(QColor("#264026"))
        self.setCaretForegroundColor(QColor("#000000"))
        self.setCaretLineVisible(True)
        lexer = QsciLexerPython()

        lexer.setDefaultFont(QFont("Consolas", 14))
        lexer.setDefaultPaper(QColor("#3c3c3c"))
        lexer.setDefaultColor(QColor("#f9f9f9"))

        lexer.setFont(QFont("Consolas", 14), 0)
        lexer.setFont(QFont("Consolas", 14), 1)
        lexer.setFont(QFont("Consolas", 14), 2)
        lexer.setFont(QFont("Consolas", 14), 3)
        lexer.setFont(QFont("Consolas", 14), 4)
        lexer.setFont(QFont("Consolas", 14), 5)
        lexer.setFont(QFont("Consolas", 14), 6)
        lexer.setFont(QFont("Consolas", 14), 7)
        lexer.setFont(QFont("Consolas", 14), 8)
        lexer.setFont(QFont("Consolas", 14), 9)
        lexer.setFont(QFont("Consolas", 14), 10)
        lexer.setFont(QFont("Consolas", 14), 11)
        lexer.setFont(QFont("Consolas", 14), 12)
        lexer.setFont(QFont("Consolas", 14), 13)
        lexer.setFont(QFont("Consolas", 14), 14)
        lexer.setFont(QFont("Consolas", 14), 15)


        lexer.setColor(QColor("#FFF"), 0)# Default = 0
        lexer.setColor(QColor("#05FE40"), 1)# Comment = 1
        lexer.setColor(QColor("#FFF"), 2)#  Number = 2#
        lexer.setColor(QColor("#E7DB74"), 3)#  DoubleQuotedString = 3#
        lexer.setColor(QColor("#B36932"), 4)# SingleQuotedString = 4#
        lexer.setColor(QColor("#FEFB02"), 5)#    Keyword = 5#
        lexer.setColor(QColor("#E7DB74"), 6)# TripleSingleQuotedString = 6#
        lexer.setColor(QColor("#E7DB74"), 7)# TripleDoubleQuotedString = 7#
        lexer.setColor(QColor("#88E22B"), 8)#  ClassName = 8#
        lexer.setColor(QColor("#FDD68A"), 9)#  FunctionMethodName = 9#
        lexer.setColor(QColor("#EC5166"), 10)#  Operator = 10#
        lexer.setColor(QColor("#60D8EF"), 11)#  Identifier = 11#
        lexer.setColor(QColor("#C5A84F"), 12)# CommentBlock = 12
        lexer.setColor(QColor("#B9644F"), 13)#  UnclosedString = 13
        lexer.setColor(QColor("#C3485C"), 14)#  HighlightedIdentifier = 14
        lexer.setColor(QColor("#498B60"), 15)# Decorator = 15

        self.setCaretForegroundColor(QColor("#000000"))
        self.setCaretWidth(5)
        self.setTabWidth(4)
        self.setIndentationGuides(True)
        self.setTabIndents(True)
        self.setAutoIndent(True)
        self.setFolding(QsciScintilla.BoxedTreeFoldStyle)
        my_list = [".", " ", "{","}","[","]","(",")", ":", ";"]
        self.setAutoCompletionWordSeparators(my_list)
        self.setLexer(lexer)
        api = Qsci.QsciAPIs(lexer)
        for key in keyword.kwlist + dir(__builtins__):
            api.add(key)
        api.add("aLongString")
        api.add("aLongerString")
        api.add("aDifferentString")
        api.add("sOmethingElse")
        api.prepare()
        self.setAutoCompletionCaseSensitivity(False)
        self.setAutoCompletionReplaceWord(False)
        self.setAutoCompletionThreshold(1)
        self.setAutoCompletionSource(Qsci.QsciScintilla.AcsAll)
        self.SendScintilla(QsciScintilla.SCI_SETHSCROLLBAR, 0)
        shortcut_ctrl_space = QShortcut(QKeySequence("Ctrl+Space"), self);
        # self.connect(shortcut_ctrl_space, SIGNAL(activated()), self,SLOT(autoCompleteFromAll()));







