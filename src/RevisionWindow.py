from PySide6.QtWidgets import QWidget
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon

class RevisionWindow(QWidget):
    signal_TodaysRevisionWindowClose = Signal(list)
    def __init__(self, dic):
        super().__init__()
        self.ui = QUiLoader().load('ui/RevisionWindow.ui')
        self.ui.setWindowTitle("Revise today's words")
        self.ui.setWindowIcon(QIcon("asset/logo.ico"))
        self.ui.closeEvent = self.closeEvent
        self.todaysDictionary = dic.getUnrevisedWord()[0]

        self.unlearndWordList = []

        self.ifWord = True
        self.ifAgain = False
        self.iterWord = 0

    def initDictionary(self, newdic):
        self.todaysDictionary = newdic.getUnrevisedWord()[0]
        self.__reviseWords()

    def initText(self):
        self.ui.pushButton_No.clicked.connect(self.handle_pushButton_No_clicked)
        self.ui.pushButton_Yes.clicked.connect(self.handle_pushButton_Yes_clicked)

        self.ui.label_TotalWords.setText(f"Total    {len(self.todaysDictionary)}")
        self.ui.label_LeftWords.setText(f"Left    {len(self.unlearndWordList)}")
        if len(self.unlearndWordList) == 0:
            self.endLearning()
        else:
            self.setWord()

    def __reviseWords(self):
        dictionaryLength = len(self.todaysDictionary)

        self.unlearndWordList = []
        for i in range(dictionaryLength):
            if self.todaysDictionary.iloc[i]['again'] == 1:
                self.unlearndWordList.append(i)

    def buildTodaysDictionary(self, newdic):
        self.todaysDictionary = newdic.getUnrevisedWord()[0]

    def handle_pushButton_No_clicked(self):
        self.ifAgain = True
        if self.ifWord == True:
            self.setExplanation()
        else:
            self.iterWord += 1
            self.ifAgain = False
            self.setWord()

    def handle_pushButton_Yes_clicked(self):
        if self.ifWord == True:
            self.setExplanation()
        else:
            if self.ifAgain == False:
                self.todaysDictionary.loc[self.todaysDictionary.index == self.unlearndWordList[self.iterWord], 'again'] = 0
                del self.unlearndWordList[self.iterWord]
            else:
                self.iterWord += 1
            self.ifAgain = False
            self.setWord()

    def setExplanation(self):
        self.ifWord = False
        word = self.todaysDictionary.iloc[self.unlearndWordList[self.iterWord]]['word']
        explanation = self.todaysDictionary.iloc[self.unlearndWordList[self.iterWord]]['explanation']
        self.ui.textBrowser_Text.setPlainText(f"{word}\n{explanation}")

    def setWord(self):
        self.ifWord = True

        self.ui.label_LeftWords.setText(f"Left    {len(self.unlearndWordList)}")

        if self.iterWord >= len(self.unlearndWordList):
            if len(self.unlearndWordList) == 0:
                self.endLearning()
                return
            else:
                self.iterWord = 0
        word = self.todaysDictionary.iloc[self.unlearndWordList[self.iterWord]]['word']
        self.ui.textBrowser_Text.setPlainText(word)

    def endLearning(self):
        self.ui.textBrowser_Text.setPlainText("Congratulation! You have revised today's words!")

        self.ui.pushButton_No.clicked.disconnect(self.handle_pushButton_No_clicked)
        self.ui.pushButton_Yes.clicked.disconnect(self.handle_pushButton_Yes_clicked)

        self.ui.pushButton_No.clicked.connect(self.closeBoth)
        self.ui.pushButton_Yes.clicked.connect(self.closeBoth)

        self.ui.pushButton_No.setText("Close")
        self.ui.pushButton_Yes.setText("Close")

    def closeBoth(self):
        self.ui.close()
        self.close()

    def closeEvent(self, event):
        returnWordList = []
        for i in range(len(self.todaysDictionary)):
            if self.todaysDictionary.iloc[i]['again'] == 0:
                returnWordList.append(self.todaysDictionary.iloc[i]['word'])
        self.signal_TodaysRevisionWindowClose.emit(returnWordList)


class RevisionFormerWindow(QWidget):
    signal_FormerRevisionWindowClose = Signal(list)
    def __init__(self, dic):
        super().__init__()
        self.ui = QUiLoader().load('ui/RevisionWindow.ui')
        self.ui.setWindowTitle("Revise former words")
        self.ui.setWindowIcon(QIcon("asset/logo.ico"))
        self.ui.closeEvent = self.closeEvent
        self.formerDictionary = dic.getUnrevisedWord()[1]

        self.unlearndWordList = []

        self.ifWord = True
        self.ifAgain = False
        self.iterWord = 0

    def initDictionary(self, newdic):
        self.formerDictionary = newdic.getUnrevisedWord()[1]
        self.__reviseWords()

    def initText(self):
        self.ui.pushButton_No.clicked.connect(self.handle_pushButton_No_clicked)
        self.ui.pushButton_Yes.clicked.connect(self.handle_pushButton_Yes_clicked)

        self.__reviseWords()
        self.ui.label_TotalWords.setText(f"Total    {len(self.formerDictionary)}")
        self.ui.label_LeftWords.setText(f"Left    {len(self.unlearndWordList)}")
        if len(self.unlearndWordList) == 0:
            self.endLearning()
        else:
            self.setWord()

    def __reviseWords(self):
        dictionaryLength = len(self.formerDictionary)
        self.unlearndWordList = []
        for i in range(dictionaryLength):
            if self.formerDictionary.iloc[i]['again'] == 1:
                self.unlearndWordList.append(i)

    def buildformerDictionary(self, newdic):
        self.formerDictionary = newdic.getUnrevisedWord()[0]

    def handle_pushButton_No_clicked(self):
        self.ifAgain = True
        if self.ifWord == True:
            self.setExplanation()
        else:
            self.iterWord += 1
            self.ifAgain = False
            self.setWord()

    def handle_pushButton_Yes_clicked(self):
        if self.ifWord == True:
            self.setExplanation()
        else:
            if self.ifAgain == False:
                self.formerDictionary.loc[self.formerDictionary.index == self.unlearndWordList[self.iterWord], 'again'] = 0
                del self.unlearndWordList[self.iterWord]
            else:
                self.iterWord += 1
            self.ifAgain = False
            self.setWord()

    def setExplanation(self):
        self.ifWord = False
        explanation = self.formerDictionary.iloc[self.unlearndWordList[self.iterWord]]['explanation']
        self.ui.textBrowser_Text.setPlainText(explanation)

    def setWord(self):
        self.ifWord = True

        self.ui.label_LeftWords.setText(f"Left    {len(self.unlearndWordList)}")

        if self.iterWord >= len(self.unlearndWordList):
            if len(self.unlearndWordList) == 0:
                self.endLearning()
                return
            else:
                self.iterWord = 0
        word = self.formerDictionary.iloc[self.unlearndWordList[self.iterWord]]['word']
        self.ui.textBrowser_Text.setPlainText(word)

    def endLearning(self):
        self.ui.textBrowser_Text.setPlainText("Congratulation! You have revised today's words!")

        self.ui.pushButton_No.clicked.disconnect(self.handle_pushButton_No_clicked)
        self.ui.pushButton_Yes.clicked.disconnect(self.handle_pushButton_Yes_clicked)

        self.ui.pushButton_No.clicked.connect(self.closeBoth)
        self.ui.pushButton_Yes.clicked.connect(self.closeBoth)

        self.ui.pushButton_No.setText("Close")
        self.ui.pushButton_Yes.setText("Close")

    def closeBoth(self):
        self.ui.close()
        self.close()

    def closeEvent(self, event):
        returnWordList = []
        for i in range(len(self.formerDictionary)):
            if self.formerDictionary.iloc[i]['again'] == 0:
                returnWordList.append(self.formerDictionary.iloc[i]['word'])
        self.signal_FormerRevisionWindowClose.emit(returnWordList)

