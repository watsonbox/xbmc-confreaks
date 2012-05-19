#!/usr/bin/env python
from xbmcswift2 import Plugin

PLUGIN_NAME = 'Confreaks'
PLUGIN_ID = 'plugin.video.confreaks'

plugin = Plugin(PLUGIN_NAME, PLUGIN_ID, __file__)


@plugin.route('/')
def index():
    item = {'label': 'RubyConf 2012', 'path': plugin.url_for('show_presentations', conference='railsconf2012')}
    return [item]


@plugin.route('/conferences/<conference>/')
def show_presentations(conference):
  # TODO: Parse the conference presentations
  items = [
      {'label': 'Keynote: Progress',
       'path': 'http://cdn.confreaks.com/system/assets/datas/3181/original/854-railsconf2012-keynote-progress-large.mp4?1335884718',
       'is_playable': True,
       }
  ]
  return items

if __name__ == '__main__':
    plugin.run()