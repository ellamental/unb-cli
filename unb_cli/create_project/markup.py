# -*- coding: utf-8 -*-
"""
A simple markup generator.

Currently this will only output ReStructured Text (rst) markup, but eventually
this will allow other forms of markup as well (like markdown, for example).

"""

def h1(val):
  return '=' * len(val)

def h2(val):
  return '-' * len(val)

def h3(val):
  return '~' * len(val)

def foo():
  print foo

def url(text, url=None):
  if not url:
    return text
  else:
    return '`' + text + ' <' + url + '>`_'

def mailto(text, address=None):
  if not address:
    address = text
  # mailto is implicit in rst
  return address
