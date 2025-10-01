#!/usr/bin/env python

"""by cgpt"""

import sys

from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import QTimer

def show_dialog():
    msg = QMessageBox()
    msg.setWindowTitle("🤖 Reality Check")
    msg.setText("❓️ Am I dreaming?")
    msg.setIcon(QMessageBox.Question)
    msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    result = msg.exec()

    if result == QMessageBox.Yes:
        # Show congrats dialog if Yes
        congrats = QMessageBox()
        congrats.setWindowTitle("🚨🚨🚨 Important Notification")
        congrats.setIcon(QMessageBox.Information)
        congrats.setText("🎉 Congratulations! You are now lucid!")
        congrats.exec()
    else:
        # aww man
        pass

g_timer = None

def start_timer():
    global g_timer
    assert g_timer is None
    g_timer = QTimer()
    g_timer.timeout.connect(show_dialog)
    g_timer.start(3 * 60 * 60 * 1000)  # 3 hours in milliseconds

def test():
    app = QApplication(sys.argv)
    show_dialog()

if __name__ == '__main__':
  test()
