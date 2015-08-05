#!/usr/bin/env python

'''
Example usage of Commands.

An easy and clean way to create commandline programs that use subcommands.

Simply decorate your command handlers with `@register` to create a parser for a
command handler, and 0 or more `@arg` decorators to add required or optional
arguments to your subcommand.

Commands is a very thin layer around argparse, for example the `@arg` decorator
essentially just calls `parser.add_argument(*args, **kwargs)` with the `args`
and `kwargs` that you pass it.  So everything you know about argparse will
translate directly to Commands.

Example:

    from commands import Group, arg

    register = Group()

    @arg('-n', '--num', type=int, default=42)
    def echo(args):
      """Usage: %(prog)s echo [-n, --num]=<int>"""
      print "Arguments: ", args
    register.command(echo)
'''

from commands import arg, Group


def cli():
  print 'UNB cli...'


register = Group(
  init_func=cli,
  title='Commands',
  description="%(prog)s is a suite of tools for managing stuff.",
)


@arg('num',
     type=int,
     help="Just a num, an ordinary num.")
@arg('-f',
     '--foo',
     action='store_true',
     help="Foo some stuff.")
@arg('-b',
     '--bar',
     nargs='?',
     type=int,
     default=5,
     help=("Bar it until you can't anymore.  "
           "(default: %(default)s, nargs: %(nargs)s, type: %(type)s).  "
           "Checkout those format specifiers!  Sweet Jebus! \n\n"
           "They're pretty..."))
@arg('--baz',
     action='store_true',
     help="Baz all the way to the bank!")
def echo(num, bar, **kwargs):
  """A one line description of the command: `%(prog)s echo` is a tool for...

  A longer description of the command.  This can overflow onto multiple
  lines, and may even be multiple paragraphs.

  Examples:

    The longer description is free to contain additional sections, such as an
    "examples" section.

       %(prog)s echo "Woo Hoo!"

  Contact:

    You may also include bug reporting or author information.

    Please report bugs to: bugs@woohoo.com
    Author: John Doe (JohnDoe@woohoo.com)
    Documentation: http://www.woohoo.com/docs
  """
  print 'num: ', num
  print 'bar: ', bar
  print 'kwargs: ', kwargs
register.command(echo)


def echo2():
  """So much echo."""
  pass
register.command(echo2)


def die():
  pass
register.command(die)


def kill():
  """Killin it.

  Softly.

  With his song.
  """
  pass
register.command(kill)


if __name__ == '__main__':
  register()
