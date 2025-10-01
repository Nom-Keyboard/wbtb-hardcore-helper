#!/usr/bin/env python

"""by cgpt"""

import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtGui import QIcon
from PySide6.QtCore import QTimer, Qt

import matching

def stub_callback_close(window: QWidget):
    print('Stub: Close Window')
    window.close()

class ReminderWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.fn_callback_close = stub_callback_close
        self.setWindowTitle("Reminder App")

        # Try to load a KDE-friendly icon, fallback if not available
        self.setWindowIcon(QIcon.fromTheme("alarm-symbolic") or QIcon.fromTheme("alarm") or QIcon.fromTheme("appointment-soon"))

        # Central widget
        central = QWidget()
        layout = QVBoxLayout(central)

        # Label for agenda text
        self.label = QLabel("", alignment=Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 18px; padding: 10px;")
        layout.addWidget(self.label)

        # Close button
        btn_close = QPushButton("Close")
        btn_close.setStyleSheet("padding: 6px; font-size: 14px;")
        btn_close.clicked.connect(self.callback_close)
        layout.addWidget(btn_close, alignment=Qt.AlignCenter)

        self.setCentralWidget(central)

        # Timer to refresh label every second
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_label)
        self.timer.start(1000)

        self.update_label()

    def update_label(self):
        self.label.setText(matching.format_current())

    def callback_close(self):
        if self.fn_callback_close is not None:
            self.fn_callback_close(self)

    def set_callback_close_fn(self, fn):
        self.fn_callback_close = fn

def test():
  app = QApplication(sys.argv)

  window = ReminderWindow()
  window.show()

  sys.exit(app.exec())

if __name__ == '__main__':
  test()
