import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
import collection

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        button = QPushButton("Press Me!")
        button.setCheckable(True)
        button.clicked.connect(self.the_button_was_clicked)

        # Set the central widget of the Window.
        self.setCentralWidget(button)

    def the_button_was_clicked(self):
        game_col = collection.Collection()
        collection.manual_game_create()
    
app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()