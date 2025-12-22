    import sys
    from PySide6.QtCore import QSize, Qt
    from PySide6.QtWidgets import (
        QApplication, 
        QMainWindow, 
        QPushButton, 
        QLabel, 
        QWidget,
        QHBoxLayout, # Imported for MainWindow's layout
        QVBoxLayout, # Imported for InputWidget's layout
        QLineEdit # Imported for InputWidget
    )

    # ==========================================================
    # 1. DEFINE THE REUSABLE WIDGET CLASS FIRST
    # ==========================================================

    class InputWidget(QWidget):
        """A self-contained widget containing a QLineEdit."""
        def __init__(self, parent=None):
            super().__init__(parent)
            
            # Create the input box
            self.input = QLineEdit()
            self.input.setPlaceholderText("Enter a new item...")
            
            # Set up a simple vertical layout for this widget
            layout = QVBoxLayout() 
            layout.addWidget(self.input)
            self.setLayout(layout)

        # Method to expose the QLineEdit's signal
        def get_input_signal(self):
            return self.input.textChanged
        
    class Button(QWidget):
        def __init__(self, parent=None, function):
            super().__init__(parent)

            self.function = function
            self.button = QPushButton("Create game")
            self.button.clicked.connect(self.function)

    # ==========================================================
    # 2. DEFINE THE MAIN WINDOW CLASS THAT USES THE WIDGET
    # ==========================================================

    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Dynamic Input App")
            
            # Initialize necessary members
            self.input_widgets = [] 
            
            # 1. Setup the main layout (Using QVBoxLayout for vertical stacking is more common 
            #    when dynamically adding items, but keeping your QHBoxLayout for now.)
            self.main_layout = QHBoxLayout()
            
            self.test_label = QLabel("Enter a game name")
            # Add the label to the beginning of the horizontal layout
            self.main_layout.addWidget(self.test_label)
            
            # 2. Create the container and set it as the central widget
            container = QWidget()
            container.setLayout(self.main_layout)
            self.setCentralWidget(container)
            
        def add_input_box(self):
            
            # 1. Create the new widget instance
            new_input_widget = InputWidget()
            
            # 2. Store a reference to the new widget
            self.input_widgets.append(new_input_widget)
            
            # 3. Add the widget to the main layout
            self.main_layout.addWidget(new_input_widget)
            
            # 4. Connect signal to a slot (must define handle_input_change first)
            new_input_widget.get_input_signal().connect(self.handle_input_change)

        def handle_input_change(self, new_text):
            print(f"Input changed to: {new_text}")


        def add_button(self):

            # create new button
            new_button = Button()

        


