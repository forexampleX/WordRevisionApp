from PySide6.QtWidgets import QApplication

from MainWindow import MainWindow
from Dictionary import Dictionary
from Schedule import Schedule

if __name__ == '__main__':
    dictionaryPath = 'db/wordDictionary.csv'
    schedulePath = 'db/schedule.csv'
    dic = Dictionary(dictionaryPath)
    sch = Schedule(schedulePath)

    app = QApplication([])
    mainwindow = MainWindow(dic, sch)
    mainwindow.ui.show()
    app.exec()