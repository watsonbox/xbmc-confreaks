#!/usr/bin/env python
import re
from xbmcswift2 import Plugin
from xbmcswift2 import download_page
from BeautifulSoup import BeautifulSoup as BS

from api.router import Router
from api.event import Event

PLUGIN_NAME = 'Confreaks'
PLUGIN_ID = 'plugin.video.confreaks'

plugin = Plugin(PLUGIN_NAME, PLUGIN_ID, __file__)

def htmlify(url):
  return BS(download_page(url))

def full_url(path):
  return 'http://www.confreaks.tv/' + path


@plugin.route('/')
def index():
  return [{
    'label': event.name() + '  [COLOR mediumslateblue]' + event.pretty_start() + ' - ' + event.pretty_end() + '[/COLOR]',
    'path': plugin.url_for('show_presentations', conference=event.code()),
    #'icon': ''
  } for event in Router.events()]


@plugin.route('/conferences/<conference>/')
def show_presentations(conference):
  html = htmlify(full_url('events/' + conference))
  events = [event.findAll('a') for event in html.findAll('div', { 'class': 'video' })]

  return [{
    'label': event_links[1].string.strip() + '  [COLOR mediumslateblue]' + (event_links[2].string.strip() if len(event_links) > 2 else '') + '[/COLOR]',
    'path': plugin.url_for('show_videos', presentation=event_links[1]['href'][event_links[1]['href'].rfind('/')+1:])
  } for event_links in events]


@plugin.route('/presentations/<presentation>/')
def show_videos(presentation):
  html = htmlify(full_url('videos/' + presentation))

  # Try Vimeo source
  iframe_src = html.find('div', { 'class': 'video-container' }).find('iframe')['src']
  vimeo_match = re.search(r'.*player\.vimeo\.com/video/(\d+).*', iframe_src)

  if vimeo_match:
    return [{
      'label': 'Vimeo Video',
      'path': 'plugin://plugin.video.vimeo/?action=play_video&videoid=' + vimeo_match.group(1),
      'is_playable': True
    }]

  # Try YouTube source
  youtube_match = re.search(r'.*youtube\.com/embed/(.+)$', iframe_src)

  if youtube_match:
    return [{
      'label': 'YouTube Video',
      'path': 'plugin://plugin.video.youtube/?action=play_video&videoid=' + youtube_match.group(1),
      'is_playable': True
    }]

  # No videos could be found
  return []


if __name__ == '__main__':
    plugin.run()