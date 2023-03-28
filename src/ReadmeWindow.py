from PySide6.QtWidgets import QDialog
from PySide6.QtUiTools import QUiLoader

class ReadmeWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = QUiLoader().load('ui/Readme.ui')
        self.ReadmeTxt = ""
        with open("db/Readme.md") as fReadme:
            self.ReadmeTxt = fReadme.read()
        self.ui.textBrowser_Readme.setMarkdown(self.ReadmeTxt)
