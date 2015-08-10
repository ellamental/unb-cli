"""A crude library of utilities used in templates."""

import textwrap


def wrap(text, fill_columns=79, indent=0, subsequent_indent=None):
  if subsequent_indent is None:
    subsequent_indent = indent
  return textwrap.fill(text,
                       width=fill_columns,
                       break_long_words=False,
                       break_on_hyphens=False,
                       initial_indent=' ' * indent,
                       subsequent_indent=' ' * subsequent_indent)


def get_block_indent(text):
  without_newlines = text.lstrip('\n')
  without_spaces = without_newlines.lstrip(' ')
  return len(without_newlines) - len(without_spaces)


def wrap_block(text, indent=0):
  """Wrap a block neatly at 79 chars, *after* it's been rendered.

  Example Template:

      Hi my name is {{ method_to_get_name_so_long_we_are_near_the_end }}.
      I really don't want a massive amount of whitespace on the line above.

  Example Rendering:

      Hi my name is Nick.
      I really don't want a massive amount of whitespace on the line above.

  Example Rendering with wrap_block:

      Hi my name is Nick. I really don't want a massive amount of whitespace
      on the line above.

  This also tries to not wrap headlines (for rst/markdown, and preserve
  indentation.  Though it's not very smart, so don't expect it to work in any
  use-case outside the explicit ones used in the ``unb-cli`` templates.
  """
  indent = get_block_indent(text)
  paragraphs = text.split('\n\n')
  ret = []
  for paragraph in paragraphs:
    lines = paragraph.strip().splitlines()
    # Very naively try not to wrap headers...
    if len(lines) == 2:
      if not lines[1].lstrip(' ').startswith(('=', '-', '~')):
        ret.append(wrap(paragraph, subsequent_indent=indent))
      else:
        ret.append(paragraph)
    else:
      ret.append(wrap(paragraph, subsequent_indent=indent))
  return '\n\n'.join(ret)


def pystr(s):
  """Output a string as an eval'able representation of a Python string."""
  return s.__repr__()
