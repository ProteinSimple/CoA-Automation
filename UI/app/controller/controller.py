class MainController:
    def __init__(self, model):
        self.model = model

    def get_text(self):
        return self.model.get_text()

    def set_text(self, new_data):
        self.model.set_text(new_data)