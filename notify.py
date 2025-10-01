#!/usr/bin/env python

"""by cgpt"""

import dbus

bus = dbus.SessionBus()
notifications = bus.get_object("org.freedesktop.Notifications",
                               "/org/freedesktop/Notifications")
notify_iface = dbus.Interface(notifications, "org.freedesktop.Notifications")

def show(message: str):
  app_name = "ReminderApp"
  replaces_id = 0
  icon = "appointment-soon"
  summary = "Reminder"
  actions = ["dismiss", "I see!"]  # action_id, label
  hints = {
      "urgency": dbus.Byte(2),        # 2 = critical, makes it pop more prominently
      "sound-file": "/usr/share/sounds/freedesktop/stereo/complete.oga",  # path to sound
  }
  timeout = 0  # 0 = persist until user interacts

  notify_iface.Notify(app_name, replaces_id, icon, summary, message, actions, hints, timeout)

def test():
  import threading

  show('Hi')
  threading.Event().wait()

if __name__ == '__main__':
  test()
