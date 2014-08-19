#!/usr/bin/env python
import sys
from PyQt5.QtWidgets import QApplication
from fly_tracker_window import FlyTrackerWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = FlyTrackerWindow()
    w.show()
    sys.exit(app.exec_())
