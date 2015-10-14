from datetime import datetime, date
import time

DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.000Z'

class Event(object):
  def __init__(self, json):
    self.display_name = json['display_name']
    self.short_code = json['short_code']
    self.conference = json['conference']
    self.start_at = self.parse_date(json['start_at'])
    self.end_at = self.parse_date(json['end_at'])

  def parse_date(self, date_string):
    try:
      return datetime.strptime(date_string, DATETIME_FORMAT)
    except TypeError:
      return datetime(*(time.strptime(date_string, DATETIME_FORMAT)[0:6]))

  # Format start date e.g. 'Jan 10'
  def pretty_start(self):
    return self.start_at.strftime('%b %d')

  # Format end date e.g. 'Jan 15'
  def pretty_end(self):
    return self.end_at.strftime('%b %d')

  # Format date range e.g. 'Jan 10 - Jan 15' or 'Jan 10' if only one day
  def pretty_range(self):
    if self.pretty_start() == self.pretty_end():
      return self.pretty_start()
    else:
      return '%s - %s' % (self.pretty_start(), self.pretty_end())

  def name(self):
    return self.display_name if self.display_name is not None else self.conference

  def code(self):
    return self.short_code.lower()
