import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi

# Create a class to load the .ui file
class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        # Load the .ui file (make sure the path to your .ui file is correct)
        loadUi('DBDAutoBloodwebGUI.ui', self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
