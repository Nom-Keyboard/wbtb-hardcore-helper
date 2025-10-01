#!/usr/bin/env python

import sys

from PySide6.QtWidgets import QApplication, QWidget

import tray
import window
import notify
import matching

class App:
  def __init__(self):
    self.app = QApplication(sys.argv)

    self.main_window = window.ReminderWindow()
    self.main_window.set_callback_close_fn(self.close_window_handler)

    self.sys_tray = tray.TrayApp(self.app)
    self.sys_tray.set_show_window_fn(self.open_window_handler)

    self.show_startup_notification()

  def run(self):
    sys.exit(self.app.exec())

  def close_window_handler(self, window: QWidget):
    window.hide()

  def open_window_handler(self):
    if self.main_window.isVisible():
      self.main_window.hide()
    else:
      self.main_window.show()

  def show_startup_notification(self):
    notify.show(matching.format_current())

def main():
  app = App()
  app.run()

if __name__ == '__main__':
  main()
