from PyQt5.QtWidgets import QApplication
import sys
from windows.window_Main import window_Main


def main():
    app = QApplication(sys.argv)
    w = window_Main()
    w.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
