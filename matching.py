#!/usr/bin/env python

"""by cgpt"""

import datetime

import schedule

def format_current():
    now = datetime.datetime.now()
    closest_event = min_diff = None
    out_buffer = []

    for event_time, event_name in schedule.schedules:
        # combine today's date with event time
        event_dt = datetime.datetime.combine(now.date(), event_time)
        diff = event_dt - now

        if diff <= datetime.timedelta(minutes=0):
            # Test if an event is in the past but within 15 minutes
            if diff >= datetime.timedelta(minutes=-15):
                out_buffer.append(f"🕓️ Just now: {event_name} ({-int(diff.total_seconds() // 60)} min ago)")
                continue

            # If the event already passed today, consider it tomorrow
            event_dt += datetime.timedelta(days=1)
            diff = event_dt - now

        # Find the next closest event
        if min_diff is None or diff < min_diff:
            min_diff = diff
            closest_event = event_name

    if closest_event is not None:
        minutes = int(min_diff.total_seconds() // 60)
        seconds = int(min_diff.total_seconds() % 60)
        out_buffer.append(f'🗓️ Next: "{closest_event}" in {minutes}min {seconds}sec')

    if len(out_buffer) > 0:
        return '\n'.join(out_buffer)

    return "✅️ No upcoming events."

def test():
  print(format_current())

if __name__ == '__main__':
  test()

