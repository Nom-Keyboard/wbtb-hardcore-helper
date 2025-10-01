#!/usr/bin/env python

"""by cgpt"""

import sys

from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import QTimer

import matching

def stub_show_window():
    print("Stub: Show window")

class TrayApp:
    def __init__(self, app: QApplication):
        self.app = app
        self.fn_show_window = stub_show_window

        # Ensure the app doesn't exit when last window closes
        self.app.setQuitOnLastWindowClosed(False)

        # Use KDE Breeze alarm icon
        icon = QIcon.fromTheme("alarm")
        if icon.isNull():
            icon = QIcon.fromTheme("clock")  # just in case

        # Create tray icon
        self.tray_icon = QSystemTrayIcon(icon, parent=self.app)

        # Context menu
        self.menu = QMenu()

        self.open_action = QAction("Show Status")
        self.open_action.triggered.connect(self.callback_show_window)
        self.menu.addAction(self.open_action)

        self.quit_action = QAction("Quit")
        self.quit_action.triggered.connect(self.callback_quit)
        self.menu.addAction(self.quit_action)

        self.tray_icon.setContextMenu(self.menu)

        # Left-click triggers callback_show_window
        self.tray_icon.activated.connect(self.on_tray_activated)

        # Tooltip update every second
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_tooltip)
        self.timer.start(1000)

        self.tray_icon.show()
        self.update_tooltip()  # set initial tooltip

    def update_tooltip(self):
        self.tray_icon.setToolTip(matching.format_current())

    def on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:  # left-click
            self.callback_show_window()

    def callback_quit(self):
        print("Exiting...")
        self.app.quit()

    def callback_show_window(self):
        if self.fn_show_window is not None:
            self.fn_show_window()

    def set_show_window_fn(self, fn):
        self.fn_show_window = fn

def test():
    app = QApplication(sys.argv)
    _ = TrayApp(app)
    sys.exit(app.exec())

if __name__ == '__main__':
    test()
