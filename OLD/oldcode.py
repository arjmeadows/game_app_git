import ui
import sys
import collection
import database
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QWidget


# initialise databse
database.create_db()

# set up UI
app = QApplication(sys.argv)
main_window = ui.MainWindow(800, 600)
main_window.show()
game_input = main_window.add_input_box()
add_game_button = main_window.add_button("Add game", collection.manual_game_create())

sys.exit(app.exec())


# launch core function
game_col = collection.Collection()

print("What would you like to do?")

choice = int(input("To add a game, press 1. To remove a game, press 2. To see game list, press 3: "))

if choice == 1: # this needs to become a function i think
    collection.manual_game_create()
elif choice == 2:
    collection.manual_game_remove()
elif choice == 3:
    collection.Collection.list_games()
else:
    print("That is not a valid request.")

