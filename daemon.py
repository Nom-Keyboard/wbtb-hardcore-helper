#!/usr/bin/env python

"""by cgpt"""

import threading
import datetime
import time

import dbus
from gi.repository import GLib
from dbus.mainloop.glib import DBusGMainLoop

import notify

def callback(event_name):
    notify.show(f"⏰️ Reaching time: {event_name}")

# Shared state
started = False
dbus_ready = threading.Event()
last_checked = datetime.datetime(2000, 1, 1, 0, 0, 0)
sleeping = False
lock = threading.Lock()

def format_now() -> str:
  return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def handle_sleep_signal(sleeping_now):
    global sleeping, last_checked
    if sleeping_now:
        with lock:
            sleeping = sleeping_now
        print(f"[{format_now()}] System is going to sleep...")
    else:
        with lock:
            # Reset last_checked to now, avoid calling skipped callbacks
            last_checked = datetime.datetime.now()
            sleeping = sleeping_now
        print(f"[{format_now()}] System just woke up!")

def time_watcher(schedules):
    global last_checked
    while True:
        lock.acquire()

        now = datetime.datetime.now()

        if sleeping:
            last_checked = now  # Skip checking during sleep

            lock.release()

            time.sleep(1)
            continue

        for event_time, event_name in schedules:
            trigger_datetime = datetime.datetime.combine(now.date(), event_time)

            # Only call if the target time is between last_checked and now
            if last_checked <= trigger_datetime <= now:
                threading.Thread(target=callback, args=(event_name,), daemon=True).start()
                break

        last_checked = now

        lock.release()

        time.sleep(1)  # Check every second

def start_daemon(schedules):
  global started, last_checked
  assert not started
  last_checked = datetime.datetime.now()
  # Start DBus thread
  threading.Thread(target=dbus_thread, daemon=True).start()
  dbus_ready.wait()
  # Start the daemon watcher thread
  thread = threading.Thread(target=time_watcher, args=(schedules,), daemon=True)
  thread.start()
  started = True

def dbus_thread():
  # Setup DBus sleep handler
  DBusGMainLoop(set_as_default=True)
  bus = dbus.SystemBus()
  bus.add_signal_receiver(handle_sleep_signal,
                          dbus_interface="org.freedesktop.login1.Manager",
                          signal_name="PrepareForSleep")
  loop = GLib.MainLoop()
  dbus_ready.set()
  loop.run()

def test():
  now = datetime.datetime.now()
  test_dt = now + datetime.timedelta(seconds=5)

  start_daemon([
    (test_dt.time(), 'Test'),
  ])
  threading.Event().wait()

if __name__ == '__main__':
  test()
