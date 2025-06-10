from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QWidget
from PyQt6.QtGui import QPixmap
from pathlib import Path

class TopView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout(self)

        self.icon = QLabel()
        image_path = Path(__file__).parent / "res" / "images" / "ProteinSimple-horiz-main.png"
        self.icon.setPixmap(QPixmap(str(image_path)))
        layout.addWidget(self.icon)

class MainView(QMainWindow):
    def __init__(self, controller, model):
        super().__init__()
        self.controller = controller
        self.model = model

        self.setWindowTitle("COAT")
        self._setup()
        self._connect_signals()
    def _setup(self):
        central_widget = QWidget()
        self.setStyleSheet(open("app/views/main.qss", mode='r').read())
        layout = QVBoxLayout()

        # self.top_view = TopView()
        # layout.addWidget(self.top_view)

        self.input =  QLineEdit()
        self.input.setPlaceholderText(" Enter cartridge ID here ")
        layout.addWidget(self.input)

        self.label = QLabel(self.controller.get_text())
        layout.addWidget(self.label)


        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


    def _connect_signals(self):
        self.input.textChanged.connect(self.controller.set_text)
        self.model.searchf_text.connect(self._update_from_model)

    def _update_from_model(self, new_text):
        self.label.setText(new_text)