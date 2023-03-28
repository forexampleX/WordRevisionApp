from PySide6.QtCore import QDate
import pandas as pd

class Dictionary:
    def __init__(self, dictionaryPath):
        self.dictionary = pd.read_csv(dictionaryPath)
        self.dictionaryPath = dictionaryPath
        self.dictionaryDate = QDate.fromString("2023-03-23", "yyyy-MM-dd")

    def __getFormerDateList(self, formatStr:str):
        formerDateList = []
        currentDate = QDate.currentDate()
        for days in [1, 2, 4, 7, 15]:
            aimDate = currentDate.addDays(-days).toString(formatStr)
            formerDateList.append(aimDate)
        return formerDateList

    def addWord(self, newWord, date, wordExplaination):
        newWordLine = pd.DataFrame({'word':newWord, 'date':date, 'explanation':wordExplaination, 'again':1}, index=[0])
        self.dictionary = pd.concat([self.dictionary, newWordLine], ignore_index=True)

    def saveDictionary(self):
        self.dictionary.to_csv(path_or_buf= self.dictionaryPath, mode= 'w', index = False)

    def get7DaysWordNumber(self):
        searchList = list(self.dictionary.date)
        currentDate = QDate.currentDate()
        dateNameList = []
        dateNumberList = []
        for i in range(7):
            formerDate = currentDate.addDays(i-6).toString("yyyy/M/dd")
            dateNameList.append(currentDate.addDays(i-6).toString("MM-dd"))
            dateNumberList.append(searchList.count(formerDate))

        return dateNameList, dateNumberList

    def getUnrevisedWord(self):
        todaysWordDictionary = pd.DataFrame(columns= self.dictionary.columns.to_list())
        formerWordDictionary = pd.DataFrame(columns= self.dictionary.columns.to_list())

        currentDate = QDate.currentDate()
        formerDateList = self.__getFormerDateList("yyyy/M/dd")

        for i in range(len(self.dictionary)):
            wordDict = pd.DataFrame(
                {"word": self.dictionary.iloc[i]['word'], 'date': self.dictionary.iloc[i]['date'],
                 'explanation': self.dictionary.iloc[i]['explanation'], 'again': self.dictionary.iloc[i]['again']},
                index=[0])
            if self.dictionary.iloc[i]['date'] == currentDate.toString("yyyy/M/dd"):
                todaysWordDictionary = pd.concat([todaysWordDictionary, wordDict], ignore_index=True)
            elif self.dictionary.iloc[i]['date'] in formerDateList:
                formerWordDictionary = pd.concat([formerWordDictionary, wordDict], ignore_index=True)

        return todaysWordDictionary, formerWordDictionary

    def getUnrevisedWordNumber(self):
        todaysWordDictionary, formerWordDictionary = self.getUnrevisedWord()
        return len(todaysWordDictionary), len(formerWordDictionary), todaysWordDictionary['again'].sum(), formerWordDictionary['again'].sum()

    def updateFormerWordsAgain(self):
        formerDateList = self.__getFormerDateList("yyyy/M/dd")
        for date in formerDateList:
            self.dictionary.loc[self.dictionary.date == date, 'again'] = 1
        self.saveDictionary()




