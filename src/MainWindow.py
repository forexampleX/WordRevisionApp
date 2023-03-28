from PySide6.QtWidgets import QMainWindow, QMessageBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QDate
from PySide6.QtGui import QIcon, QFont

import datetime

from ReadmeWindow import ReadmeWindow
from DrawDictionary import DrawDictionary
from RevisionWindow import RevisionWindow, RevisionFormerWindow



import ctypes
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")

class MainWindow(QMainWindow):
    def __init__(self, dic, sch):
        super(MainWindow, self).__init__()
        self.dictionary = dic
        self.schedule = sch
        self.ui = QUiLoader().load('ui/MainWindow.ui')

        self.schedule.setRevised()
        self.schedule.saveSchedule()
        self.__initFormerWords()

        self.reviseToday = RevisionWindow(self.dictionary)
        self.reviseFormer = RevisionFormerWindow(self.dictionary)
        self.drawDictionary = DrawDictionary(self.dictionary)
        self.ui.setWindowIcon(QIcon("asset/logo.ico"))


        self.ui.horizontalLayout_Graph.addWidget(self.drawDictionary, 4)
        self.__fontHead = "<font color=\"#008080\">"
        self.__fontTail = "</font>"
        self.__fontText = QFont()
        self.__fontButton = QFont()
        self.__fontText.setPointSize(12)
        self.__fontButton.setPointSize(16)
        self.__fontButton.setBold(True)
        self.ui.textBrowserInformationDisplay.setFont(self.__fontText)
        self.ui.lineEdit_Word.setFont(self.__fontText)
        self.ui.plainTextEdit_Explanation.setFont(self.__fontText)
        self.ui.textBrowser_DisplayDialogs.setFont(self.__fontText)
        self.ui.lineEdit_InputOperations.setFont(self.__fontText)
        self.ui.plainTextEdit_Input.setFont(self.__fontText)
        self.ui.pushButton_Add.setFont(self.__fontButton)
        self.ui.pushButton_Operate.setFont(self.__fontButton)
        self.ui.pushButton_Refrash.setFont(self.__fontButton)
        self.ui.pushButton_ReviseFormer.setFont(self.__fontButton)
        self.ui.pushButton_ReviseToday.setFont(self.__fontButton)

        self.showInformation()

        self.ui.actionDeveloper.triggered.connect(self.handle_actionDeveloper_triggered)
        self.ui.actionReadme.triggered.connect(self.handle_actionReadme_triggered)
        self.ui.pushButton_Add.clicked.connect(self.handle_pushButton_Add_clicked)
        self.ui.pushButton_Operate.clicked.connect(self.handle_pushButton_Operate_clicked)
        self.ui.pushButton_Refrash.clicked.connect(self.handle_pushButton_Refrash_clicked)
        self.ui.pushButton_ReviseToday.clicked.connect(self.handle_pushButton_ReviseToday_clicked)
        self.ui.pushButton_ReviseFormer.clicked.connect(self.handle_pushButton_ReviseFormer_clicked)


        self.reviseToday.signal_TodaysRevisionWindowClose.connect(self.handle_signal_TodaysRevisionWindowClose)
        self.reviseFormer.signal_FormerRevisionWindowClose.connect(self.handle_signal_FormerRevisionWindowClose)

    def __initFormerWords(self):
        ifTodayRevised, ifFormerRevised = self.schedule.get_ifRevised()
        if ifFormerRevised == 0:
            self.dictionary.updateFormerWordsAgain()

    def showInformation(self):
        self.ui.textBrowserInformationDisplay.append(self.__fontHead + 'Welcome!' + self.__fontTail + '\n')
        self.ui.textBrowserInformationDisplay.append(
            self.__fontHead + 'Today is ' + QDate.currentDate().toString('yyyy-MM-dd') + self.__fontTail + '\n')
        self.ui.textBrowserInformationDisplay.append(
            self.__fontHead + 'Please input a new word and its explanation.' + self.__fontTail + '\n')

        todaysNumber, formerNumber, todaysRevisedNumber, formerRevisedNumber = self.dictionary.getUnrevisedWordNumber()
        self.ui.textBrowser_LearningInformation.setPlainText(f"Today's Words:\n{todaysRevisedNumber} \\ {todaysNumber}\n\n\nFormer Words:\n{formerRevisedNumber} \\ {formerNumber}")

    def handle_actionDeveloper_triggered(self):
        QMessageBox.about(self, "Deveolper Information", "Developed by Zhuo Dai, BIT, 2023-03-28")

    def handle_actionReadme_triggered(self):
        self.readmeWindow = ReadmeWindow()
        self.readmeWindow.ui.show()

    def handle_pushButton_Add_clicked(self):
        newWord = (self.ui.lineEdit_Word.text()).strip()
        newWordExplanation = (self.ui.plainTextEdit_Explanation.toPlainText()).strip()

        if newWord == "" or newWordExplanation == "":
            self.ui.textBrowserInformationDisplay.append(
                self.__fontHead + 'Please input a new word and its expanation' + self.__fontTail + '\n')

            self.ui.lineEdit_Word.setText("")
            self.ui.plainTextEdit_Explanation.setPlainText("")

        elif newWord in list(self.dictionary.dictionary.word):
            wordDate = self.dictionary.dictionary.loc[self.dictionary.dictionary.word == newWord, 'date']
            daysAgo = wordDate.daysTo(QDate.currentDate())

            self.ui.textBrowserInformationDisplay.append(self.__fontHead + 'You have learned ' + self.__fontTail+ newWord + self.__fontHead + ' on ' + self.__fontTail+ wordDate + self.__fontHead + "  (" + self.__fontTail + str(daysAgo) + self.__fontHead + ' days ago)' + self.__fontTail + "\n")
            self.ui.lineEdit_Word.setText("")
            self.ui.plainTextEdit_Explanation.setPlainText("")

        else:
            date = QDate.currentDate().toString("yyyy/M/dd")
            self.dictionary.addWord(newWord, date, newWordExplanation)
            self.ui.textBrowserInformationDisplay.append(self.__fontHead + 'Word '+ self.__fontTail + newWord + self.__fontHead + ' has been added to the dictionary!' + self.__fontTail + "\n")
            self.ui.lineEdit_Word.setText("")
            self.ui.plainTextEdit_Explanation.setPlainText("")
            self.dictionary.saveDictionary()

    def handle_pushButton_Operate_clicked(self):
        operationInput = self.ui.lineEdit_InputOperations.text()
        self.ui.textBrowser_DisplayDialogs.append(
            self.__fontHead + "-   OPERATION: " + self.__fontTail + operationInput + '\n')
        try:
            operationHead, operationTail = operationInput.split(" ", 1)
        except Exception:
            self.ui.textBrowser_DisplayDialogs.append(
                self.__fontHead + "    Please input a correct operation" + self.__fontTail + '\n')
            operationHead, operationTail = " ", " "
        else:
            operationTail = operationTail.strip()
            if operationHead == "SELECT":
                searchListLen = len((self.dictionary.dictionary['word']).tolist())
                builtDate = self.dictionary.dictionaryDate.toString("yyyy-MM-dd ddd")
                if operationTail == "ALL":
                    self.ui.textBrowser_DisplayDialogs.append(self.__fontHead + "    The dictionary has " + self.__fontTail + str(searchListLen) + self.__fontHead + " words" + self.__fontTail + '\n')
                    for word in (self.dictionary.dictionary['word']).tolist():
                        self.ui.textBrowser_DisplayDialogs.append("    " + word)
                elif operationTail == "INFO":
                    self.ui.textBrowser_DisplayDialogs.append(self.__fontHead + "    The dictionary is built at "+ self.__fontTail + builtDate + '\n')
                    self.ui.textBrowser_DisplayDialogs.append(self.__fontHead + "    The dictionary has " + self.__fontTail + str(searchListLen) + self.__fontHead + " words" + self.__fontTail + '\n')
                else:
                    wordSearched = operationTail
                    searchList = (self.dictionary.dictionary['word']).tolist()
                    searchListLen = len(searchList)
                    wordItem = -1
                    for i in range(searchListLen):
                        if searchList[i] == wordSearched:
                            wordItem = i
                            break
                    if wordItem == -1:
                        self.ui.textBrowser_DisplayDialogs.append(
                            wordSearched + self.__fontHead + " is not in the dictionary." + self.__fontTail + '\n')
                    else:
                        wordDate = (self.dictionary.dictionary.iloc[wordItem]).loc['date']
                        wordExplanation = (self.dictionary.dictionary.iloc[wordItem]).loc['explanation']
                        self.ui.textBrowser_DisplayDialogs.append("    " + wordSearched + '\n' + "    " + wordDate + '\n' + "    " + wordExplanation + '\n')

                        self.ui.plainTextEdit_Input.setPlainText(wordExplanation)

            elif operationHead == "DROP":
                wordSearched = operationTail
                if wordSearched in list(self.dictionary.dictionary.word):
                    self.dictionary.dictionary.drop(
                        self.dictionary.dictionary[self.dictionary.dictionary.word == wordSearched].index, inplace=True)
                    self.ui.textBrowser_DisplayDialogs.append(
                        self.__fontHead + "Successfully delete " + self.__fontTail + wordSearched + '\n')
                else:
                    self.ui.textBrowser_DisplayDialogs.append(
                        wordSearched + self.__fontHead + " is not in the dictionary." + self.__fontTail + '\n')

            elif operationHead == "UPDATE":
                if operationTail == "BEGINDATE":
                    beginDate = self.ui.plainTextEdit_Input.toPlainText().strip()
                    try:
                        correctBeginDate = datetime.date.fromisoformat(beginDate)
                    except Exception as error:
                        self.ui.textBrowser_DisplayDialogs.append(
                            self.__fontHead + "Illegal date:" + self.__fontTail + str(error) + '\n')
                    else:
                        self.dictionary.dictionaryDate = QDate.fromString(beginDate, "yyyy-MM-dd")
                        self.ui.textBrowser_DisplayDialogs.append(
                            self.__fontHead + "    The dictionary is rebuilt at " + self.__fontTail + beginDate + '\n')
                    finally:
                        self.ui.plainTextEdit_Input.setPlainText("")
                else:
                    wordSearched = operationTail
                    if wordSearched in list(self.dictionary.dictionary.word):
                        wordExplanation = (self.ui.plainTextEdit_Input.toPlainText()).strip()
                        self.dictionary.dictionary.loc[
                            self.dictionary.dictionary.word == wordSearched, 'explanation'] = wordExplanation
                        self.ui.textBrowser_DisplayDialogs.append(
                            wordSearched + self.__fontHead + " 's explanation has been updated to " + self.__fontTail + wordExplanation + '\n')
                        self.ui.plainTextEdit_Input.setPlainText("")
                    else:
                        self.ui.textBrowser_DisplayDialogs.append(
                            wordSearched + self.__fontHead + " is not in the dictionary." + self.__fontTail + '\n')

            else:
                self.ui.textBrowser_DisplayDialogs.append(
                    self.__fontHead + "Please input correct operation." + self.__fontTail + '\n')
        finally:
            self.dictionary.saveDictionary()
            self.ui.lineEdit_InputOperations.setText("")

    def handle_pushButton_Refrash_clicked(self):
        todaysNumber, formerNumber, todaysRevisedNumber, formerRevisedNumber = self.dictionary.getUnrevisedWordNumber()
        self.ui.textBrowser_LearningInformation.setPlainText(
            f"Today's Words:\n{todaysRevisedNumber} \\ {todaysNumber}\n\n\nFormer Words:\n{formerRevisedNumber} \\ {formerNumber}")
        self.drawDictionary.drawDic()

    def handle_pushButton_ReviseToday_clicked(self):
        self.schedule.setRevised(0)
        self.reviseToday.initDictionary(self.dictionary)
        self.reviseToday.ui.show()
        self.reviseToday.initText()
        self.ui.showMinimized()

    def handle_pushButton_ReviseFormer_clicked(self):
        self.schedule.setRevised(1)
        self.reviseFormer.initDictionary(self.dictionary)
        self.reviseFormer.ui.show()
        self.reviseFormer.initText()
        self.ui.showMinimized()

    def handle_signal_TodaysRevisionWindowClose(self, unrevisedWordList):
        self.ui.showNormal()

        for word in unrevisedWordList:
            self.dictionary.dictionary.loc[
                self.dictionary.dictionary.word == word, 'again'] = 0
        self.dictionary.saveDictionary()
        self.handle_pushButton_Refrash_clicked()

    def handle_signal_FormerRevisionWindowClose(self, revisedWordList):
        self.ui.showNormal()

        for word in revisedWordList:
            self.dictionary.dictionary.loc[
                self.dictionary.dictionary.word == word, 'again'] = 0
        self.dictionary.saveDictionary()
        self.handle_pushButton_Refrash_clicked()