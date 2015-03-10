#!/usr/bin/env python
from xbmcswift2 import Plugin
from xbmcswift2 import download_page
from api.router import Router

PLUGIN_NAME = 'Confreaks'
PLUGIN_ID = 'plugin.video.confreaks'

plugin = Plugin(PLUGIN_NAME, PLUGIN_ID, __file__)


@plugin.route('/')
def index():
  return [{
    'label': event.name() + '  [COLOR mediumslateblue]' + event.pretty_start() + ' - ' + event.pretty_end() + '[/COLOR]',
    'path': plugin.url_for('show_presentations', conference=event.code()),
    #'icon': ''
  } for event in Router.events()]


@plugin.route('/conferences/<conference>/')
def show_presentations(conference):
  return [{
    'label': video.title + '  [COLOR mediumslateblue]' + video.presenter_names() + '[/COLOR]',
    'path': plugin.url_for('show_videos', presentation=video.slug)
  } for video in Router.videos(conference)]


@plugin.route('/presentations/<presentation>/')
def show_videos(presentation):
  video = Router.video(presentation)

  if video.host() == 'vimeo':
    return [{
      'label': 'Vimeo Video',
      'path': video.url(),
      'is_playable': True
    }]
  elif video.host() == 'youtube':
    return [{
      'label': 'YouTube Video',
      'path': video.url(),
      'is_playable': True
    }]

  # No videos could be found
  return []


if __name__ == '__main__':
    plugin.run()