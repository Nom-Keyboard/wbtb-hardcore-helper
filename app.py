#!/usr/bin/env python

import sys
import signal

from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import QCoreApplication, QCommandLineParser

import tray
import window
import notify
import matching
import daemon
import schedule

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

def signal_handler(sig, frame):
    print("\nCtrl+C detected! Exiting gracefully...")
    sys.exit(0)

def main():
  # Set application info for --help output
  core_app = QCoreApplication(sys.argv)
  core_app.setApplicationName("Reminder App")
  core_app.setApplicationVersion("0.1")

  # Create CLI parser
  parser = QCommandLineParser()
  parser.setApplicationDescription("Reminder App")
  parser.addHelpOption()
  parser.addVersionOption()

  # Process the actual command-line arguments
  parser.process(core_app)

  core_app.shutdown()
  app = App()
  daemon.start_daemon(schedule.schedules)
  # Register handler for keyboard interrupts
  signal.signal(signal.SIGINT, signal_handler)
  print("Running... Press Ctrl+C to exit.")
  app.run()

if __name__ == '__main__':
  main()
