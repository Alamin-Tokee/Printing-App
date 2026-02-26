import sys
from PyQt6.QtWidgets import QApplication
from ui_main import MainWindow
import database


def main():
    database.create_table()

    app = QApplication(sys.argv)

    with open("resources.qss", "r") as f:
        app.setStyleSheet(f.read())

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()