class Video(object):
  def __init__(self, json):
    self.id = json['id']
    self.slug = json['slug']
    self.title = json['title']
    self.presenters = json['presenters']

  def presenter_names(self):
    return ', '.join(map(lambda p: p['first_name'] + ' ' + p['last_name'], self.presenters))