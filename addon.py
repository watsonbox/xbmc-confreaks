#!/usr/bin/env python
from xbmcswift2 import Plugin
from xbmcswift2 import download_page
from BeautifulSoup import BeautifulSoup as BS

PLUGIN_NAME = 'Confreaks'
PLUGIN_ID = 'plugin.video.confreaks'

plugin = Plugin(PLUGIN_NAME, PLUGIN_ID, __file__)

def htmlify(url):
  return BS(download_page(url))

def full_url(path):
  return 'http://www.confreaks.com/' + path


@plugin.route('/')
def index():
  html = htmlify(full_url('events'))
  events = [event.findAll('a')[0] for event in html.findAll('li', { 'class': 'event-box' })]

  return [{
    'label': event.string.strip(),
    'path': plugin.url_for('show_presentations', conference=event['href'][event['href'].rfind('/')+1:]),
  } for event in events]


@plugin.route('/conferences/<conference>/')
def show_presentations(conference):
  html = htmlify(full_url('events/' + conference))
  events = [event.findAll('a')[1] for event in html.findAll('div', { 'class': 'video' })]

  return [{
    'label': event.string.strip(),
    'path': plugin.url_for('show_videos', presentation=event['href'][event['href'].rfind('/')+1:]),
  } for event in events]


@plugin.route('/presentations/<presentation>/')
def show_videos(presentation):
  html = htmlify(full_url('videos/' + presentation))
  events = html.find('div', { 'class': 'video-details' }).findAll('a')

  return [{
    'label': event.string.strip(),
    'path': event['href'],
    'is_playable': True
  } for event in events]


if __name__ == '__main__':
    plugin.run()