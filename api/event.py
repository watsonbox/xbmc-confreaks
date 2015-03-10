from datetime import datetime, date

DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.000Z'

class Event(object):
  def __init__(self, json):
    self.display_name = json['display_name']
    self.short_code = json['short_code']
    self.conference = json['conference']
    self.start_at = datetime.strptime(json['start_at'], DATETIME_FORMAT)
    self.end_at = datetime.strptime(json['end_at'], DATETIME_FORMAT)

  def pretty_start(self):
    return self.start_at.strftime('%b %d')

  def pretty_end(self):
    return self.end_at.strftime('%b %d')

  def name(self):
    return self.display_name if self.display_name is not None else self.conference

  def code(self):
    return self.short_code.lower()
