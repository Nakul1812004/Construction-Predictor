from PySide6.QtWidgets import QApplication
from ui.login_window import LoginWindow
import sys

app = QApplication(sys.argv)
window = LoginWindow()
window.show()
sys.exit(app.exec())
