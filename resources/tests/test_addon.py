#!/usr/bin/env python
# Run these integration tests with 'python -m unittest discover'
import sys, os
import unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from addon import plugin, index, show_presentations, show_videos, htmlify, full_url

class IntegrationTests(unittest.TestCase):

  def test_show_presentations(self):
    items = show_presentations('arrrrcamp2013')

    # There are 22 presentations for ArrrrCamp 2013
    self.assertEqual(len(items), 22)

    # The first is 'You gotta try this'
    self.assertEqual(items[0], {
      'label': u'You gotta try this  [COLOR mediumslateblue]Avdi  Grimm[/COLOR]',
      'path': 'plugin://plugin.video.confreaks/presentations/arrrrcamp2013-you-gotta-try-this/'
    })


  def test_show_youtube_videos(self):
    items = show_videos('arrrrcamp2013-you-gotta-try-this')

    # 'You gotta try this' has a YouTube video
    self.assertEqual(len(items), 1)
    self.assertEqual(items[0], {
      'is_playable': True,
      'label': 'YouTube Video',
      'path': 'plugin://plugin.video.youtube/?action=play_video&videoid=sVd4p6oKeUA'
    })

  def test_show_vimeo_videos(self):
    items = show_videos('webrebels2012-application-cache-douchebag')

    # 'Application Cache Douchebag' has a Vimeo video
    self.assertEqual(len(items), 1)
    self.assertEqual(items[0], {
      'is_playable': True,
      'label': 'Vimeo Video',
      'path': 'plugin://plugin.video.vimeo/?action=play_video&videoid=43336762'
    })


# Commented because this presentation is not available - are any that have single files?
  # def test_show_direct_videos(self):
  #   items = show_videos('760-rubymidwest2011-mastering-the-ruby-debugger')

  #   # 'Mastering the Ruby Debugger' has multiple direct videos
  #   self.assertEqual(len(items), 4)
  #   self.assertEqual(items[0], {
  #     'is_playable': True,
  #     'label': '1920x1080 -  - application/x-mp4 - 1.2 GB - 00:34:05',
  #     'path': 'http://cdn.confreaks.com/system/assets/datas/2930/original/d2-01-mastering-the-ruby-debugger.mp4?1326174735'
  #   })
  #   self.assertEqual(items[1], {
  #     'is_playable': True,
  #     'label': '1280x720 - application/x-mp4 - 153.3 MB - 00:34:05',
  #     'path': 'http://cdn.confreaks.com/system/assets/datas/2959/original/760-rubymidwest2011-mastering-the-ruby-debugger-large.mp4?1326186609'
  #   })
  #   self.assertEqual(items[2], {
  #     'is_playable': True,
  #     'label': '640x360 -  - application/x-mp4 - 62.8 MB - 00:34:05',
  #     'path': 'http://cdn.confreaks.com/system/assets/datas/2958/original/760-rubymidwest2011-mastering-the-ruby-debugger-small.mp4?1326186603'
  #   })
  #   self.assertEqual(items[3], {
  #     'is_playable': True,
  #     'label': 'application/x-mp3 - 16.4 MB - 00:34:05',
  #     'path': 'http://cdn.confreaks.com/system/assets/datas/2960/original/760-rubymidwest2011-mastering-the-ruby-debugger.mp3?1326186611'
  #   })


  def test_index(self):
    items = index()
    rubyConf2014 = [i for i in items if i['path'] == "plugin://plugin.video.confreaks/conferences/rubyconf2014/"][0]

    # There should be more than 27 events on the first page
    self.assertTrue(len(items) == 27)

    # Ensure RubyConf 2014 data is correct
    self.assertEqual(rubyConf2014, {
      'label': u'Ruby Conference 2014  [COLOR mediumslateblue]Nov 17 - Nov 19[/COLOR]',
      'path': 'plugin://plugin.video.confreaks/conferences/rubyconf2014/',
      'icon': u'http://s3-us-west-2.amazonaws.com/confreaks-tv3/production/events/logos/000/000/225/rubyconf-website-small-thumb.png?1422307583',
    })


if __name__ == '__main__':
    unittest.main()