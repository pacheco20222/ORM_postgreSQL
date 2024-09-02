from PyQt5.QtWidgets import QApplication
from gui import AuthenticationWindow
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    auth_window = AuthenticationWindow()
    auth_window.show()
    sys.exit(app.exec_())