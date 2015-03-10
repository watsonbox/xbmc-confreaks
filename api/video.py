class Video(object):
  def __init__(self, json):
    self.id = json['id']
    self.slug = json['slug']
    self.title = json['title']
    self.presenters = json['presenters']
    self.youtube_code = json['youtube_code']

  def presenter_names(self):
    return ', '.join(map(lambda p: p['first_name'] + ' ' + p['last_name'], self.presenters))

  def host(self):
    if self.youtube_code.startswith('vimeo'):
      return 'vimeo'
    else:
      return 'youtube'

  def code(self):
    return self.youtube_code.replace('vimeo|', '')

  def url(self):
    if self.host() == 'vimeo':
      return 'plugin://plugin.video.vimeo/?action=play_video&videoid=%s' % self.code()
    else:
      return 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % self.code()
