from PyQt6.QtCore import QObject, pyqtSignal

class MyModel(QObject):
    searchf_text = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._text = ""
    
    def get_text(self):
        return self._text

    def set_text(self, new_data):
        if self._text != new_data:
            self._text = new_data
            self.searchf_text.emit(self._text)