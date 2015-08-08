"""
{{ verbose_name }}
{{ markup.h1(verbose_name) }}

{{ wrap(project_description) }}

"""

import os
from setuptools import setup, find_packages


PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
VERSION_FILE_PATH = os.path.join(PROJECT_DIR, 'VERSION')


# TODO(nick): Maybe find some way to have unb-cli include this.
def read_version():
  if not os.path.isfile(VERSION_FILE_PATH):
    raise EnvironmentError("Version file not found.")
  with open(VERSION_FILE_PATH) as f:
    return f.read().strip()


if __name__ == '__main__':
  setup(
    name='{{ project_name }}',
    version=read_version(),
    description={{ pystr(project_description) }},
    author={{ pystr(author) }},
    author_email={{ pystr(author_email) }},
    url={{ pystr(project_url) }},
    license={{ pystr(license) }},
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    classifiers=[
    {% for classifier in classifiers %}  {{ pystr(classifier) }},
    {% endfor %}],
  )
