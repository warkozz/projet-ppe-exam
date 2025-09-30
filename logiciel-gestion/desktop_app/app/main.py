# main.py - entrypoint
import sys
from PySide6.QtWidgets import QApplication
from app.app import FootApp

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FootApp()
    window.show()
    sys.exit(app.exec())
