import urllib2
import json

from event import Event
from video import Video

class Router(object):
  @classmethod
  def events(self):
    response = urllib2.urlopen('http://www.confreaks.tv/api/v1/events.json?sort=recent')
    return [Event(event) for event in json.load(response)]

  def videos(self, event_short_code):
    response = urllib2.urlopen('http://www.confreaks.tv/api/v1/events/%s/videos.json?sort=recent'.format(event_short_code))
    return [Video(video) for video in json.load(response)]
