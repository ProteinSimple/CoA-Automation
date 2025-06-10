import sys
from PyQt6.QtWidgets import QApplication

from app.model.model import MyModel
from app.views.main_view import MainView
from app.controller.controller import MainController

if __name__ == "__main__":
    app = QApplication(sys.argv)
    model = MyModel()
    controller = MainController(model)

    view = MainView(controller, model)
    view.show()
    
    sys.exit(app.exec())