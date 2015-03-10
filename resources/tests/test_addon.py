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

    # The eighth is 'You gotta try this'
    self.assertEqual(items[8], {
      'label': u'You gotta try this  [COLOR mediumslateblue]Avdi Grimm[/COLOR]',
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


  def test_index(self):
    items = index()
    rubyConf2014 = [i for i in items if i['path'] == "plugin://plugin.video.confreaks/conferences/rubyconf2014/"][0]

    # There should be more than 150 events in total
    self.assertTrue(len(items) > 150)

    # Ensure RubyConf 2014 data is correct
    self.assertEqual(rubyConf2014, {
      'label': u'Ruby Conference 2014  [COLOR mediumslateblue]Nov 17 - Nov 19[/COLOR]',
      'path': 'plugin://plugin.video.confreaks/conferences/rubyconf2014/',
      #'icon': u'http://s3-us-west-2.amazonaws.com/confreaks-tv3/production/events/logos/000/000/225/rubyconf-website-small-thumb.png?1422307583',
    })


if __name__ == '__main__':
    unittest.main()