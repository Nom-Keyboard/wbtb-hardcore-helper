#!/usr/bin/env python

"""by cgpt"""

import datetime

schedules = []
interval_hours = 3
alerts = [("1hr mark", -60), ("30m mark", -30), ("awake", 90)]  # minutes offset

dummy_date = datetime.date(2000, 1, 1)  # arbitrary fixed date for calculations

# generate base times every 3 hours
for i, hour in enumerate(range(0, 24, interval_hours), start=1):
    base_time = datetime.time(hour, 0)
    schedules.append((base_time, f'sleep #{i}'))

    base_datetime = datetime.datetime.combine(dummy_date, base_time)
    for label, offset in alerts:
        alert_datetime = base_datetime + datetime.timedelta(minutes=offset)
        schedules.append((alert_datetime.time(), label))

# sort by time
schedules.sort(key=lambda x: (x[0].hour, x[0].minute))

def test():
  for item in schedules:
      print(item)

if __name__ == '__main__':
  test()
