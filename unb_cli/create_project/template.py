import os

import jinja2


PACKAGE_PATH = os.path.dirname(os.path.abspath(__file__))


# Not sure what to do with this yet.. We should really construct the project
# auto-magically given a configuration file.

def get_loader(project_name):
  path = os.path.join(TEMPLATES_PATH, project_name, 'templates')
  return jinja2.Environment(loader=jinja2.FileSystemLoader(path))


class Templates(object):
  def __init__(self, project_name):
    self.loader = get_loader(project_name)

  def render(self, template_path, context=None):
    if context is None:
      context = {}
    return self.loader.get_template(template_path).render(context)

# t = Templates('django_project')
# t.render('ext.py')


