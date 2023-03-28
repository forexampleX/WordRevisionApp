from PySide6.QtCore import QDate
import pandas as pd

class Schedule:
    def __init__(self, schedulePath:str):
        self.schedulePath = schedulePath
        self.schedule = pd.read_csv(self.schedulePath)

    def saveSchedule(self):
        self.schedule.to_csv(path_or_buf= self.schedulePath, mode= 'w', index = False)

    def get_ifRevised(self):
        currentDate = QDate.currentDate().toString('yyyy/M/dd')
        if1,if2 = self.schedule.loc[self.schedule.date == currentDate, 'ifTodayRevised'], self.schedule.loc[self.schedule.date == currentDate, 'ifFormerRevised']
        return int(if1), int(if2)

    def setRevised(self, mode:int = -1):
        currentDate = QDate.currentDate().toString('yyyy/M/dd')
        if mode == 0:
            self.schedule.loc[self.schedule.date == currentDate, 'ifTodayRevised'] = 1
        elif mode == 1:
            self.schedule.loc[self.schedule.date == currentDate, 'ifFormerRevised'] = 1
        elif mode == 2:
            self.schedule.loc[self.schedule.date == currentDate, 'ifTodayRevised'] = 1
            self.schedule.loc[self.schedule.date == currentDate, 'ifFormerRevised'] = 1
        else:
            if currentDate in list(self.schedule.date):
                return
            else:
                newDateLine = pd.DataFrame({'date': currentDate, 'ifTodayRevised': 0, 'ifFormerRevised': 0},
                                           index=[0])
                self.schedule = pd.concat([self.schedule, newDateLine], ignore_index=True)
        self.saveSchedule()


