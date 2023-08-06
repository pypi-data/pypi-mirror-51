#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" test_colr.py
    Run a few tests for the Colr library.
    Besides unit tests, just running this script will show any obvious
    display bugs.
    -Christopher Welborn 08-30-2015
"""
# NOTE: There are actual tests to run, but this helps with display/formatting
#       problems. If any errors pop up while running this then something is
#       very wrong.
#       It's also a testbed for features, to see what Colr can do, and what
#       the limitations are.
import os
import random
import re
import sys

parentdir = os.path.split(os.path.abspath(sys.path[0]))[0]
if parentdir.endswith('colr'):
    # Use dev version before installed version.
    sys.path.insert(0, parentdir)

try:
    from colr import (
        __version__,
        codes,
        Colr,
        ColrControl,
        auto_disable,
        color,
        disabled,
        docopt,
        enable,
        name_data,
    )
except ImportError as ex:
    print('\nUnable to import Colr!: {}'.format(ex), file=sys.stderr)
    sys.exit(1)


NAME = 'Colr Test Run'
VERSIONSTR = '{} v. {}'.format(NAME, __version__)
SCRIPT = os.path.split(os.path.abspath(sys.argv[0]))[1]
SCRIPTDIR = os.path.abspath(sys.path[0])

USAGESTR = """{versionstr}
    Usage:
        {script} -h | -v
        {script} [-c] [-C] [NAME...]

    Options:
        NAME              : Name of display test function to run, or part of it.
                            Default: all tests are run
        -C,--colrcontrol  : Use the ColrControl class instead of Colr.
        -c,--color        : Force color use, even when piping.
        -h,--help         : Show this help message.
        -v,--version      : Show version.
""".format(script=SCRIPT, versionstr=VERSIONSTR)

# Automatically disable colors when piping output.
auto_disable()

CLASS = Colr


def main(argd):
    """ Main entry point, expects doctopt arg dict as argd. """
    global CLASS
    if argd['--colrcontrol']:
        CLASS = ColrControl

    if argd['--color']:
        enable()
    maxwidth = get_terminal_size()[0]

    testfuncs = []
    userargs = argd['NAME'] or ['.+']
    for namearg in userargs:
        testfuncs.extend(find_tests(namearg))
    if not testfuncs:
        raise InvalidArg('No tests found with: {}'.format(
            ', '.join(a for a in userargs)
        ))

    print('Running {}'.format(color(VERSIONSTR, fore='red', style='bright')))
    print('Class: {}'.format(CLASS.__name__))

    test_args = {
        'display_test_name_data': {'width': maxwidth // 20, 'namewidth': 20},
    }

    for func in sorted(testfuncs, key=lambda f: f.__name__):
        customargs = test_args.get(func.__name__, {'maxwidth': maxwidth})
        func(**customargs)

    if disabled():
        print('\nColr was disabled.')
    return 0


def display_test_custom_class(maxwidth=80):
    """ Test display of custom classes with __colr__ methods. """
    cl = CustomUserClass(msg='This is a test.', value=35)
    print('   {} with arguments: {}'.format(
        type(cl).__name__,
        CLASS(cl, fore='red', style='bright'),
    ))
    print('{} without arguments: {}'.format(
        type(cl).__name__,
        CLASS(cl),
    ))


def display_test_gradient_mix(maxwidth=80):
    """ Test display of the gradient options. """
    # Gradient should operate on self.data when no text is provided.
    print(CLASS('This is a gradient self.data.').gradient())

    # Gradient should append to self.data when no text is provided.
    print(
        CLASS('This is a green self.data', fore='green')(' ')
        .gradient('And this is an appended gradient.', name='blue'))

    # Gradient should be okay with ljust/center/rjust.
    print(CLASS().gradient('This is a left gradient').ljust(maxwidth))
    print(CLASS().gradient('Center gradient.').center(maxwidth))
    print(CLASS().gradient('Right-aligned gradient.').rjust(maxwidth))

    # Gradient and ljust/center/rjust would be chainable.
    chunkwidth = maxwidth / 3
    print(CLASS()
          .ljust(chunkwidth, text='Chained left.').gradient(name='red')
          .center(chunkwidth, text='Chained center.').gradient(name='white')
          .rjust(chunkwidth, text='Chained right.').gradient(name='blue'))

    # Black/white gradient should work in linemode or non-linemode.
    lines = ['This is a block made into a sad rainbow' for _ in range(5)]
    print(CLASS('\n'.join(lines)).gradient(name='black'))
    lines = ['This is a block made into a long sad rainbow' for _ in range(5)]
    print(CLASS('\n'.join(lines)).gradient(name='white', linemode=False))
    lines = ['This is a block made into a better rainbow' for _ in range(5)]
    print(CLASS('\n'.join(lines)).gradient(name='red'))


def display_test_gradient_override(maxwidth=80):
    """ Test gradient with explicit fore, back, and styles. """
    try:
        # Both fore and back are not allowed in a gradient.
        print(CLASS().gradient(' ' * maxwidth, fore='reset', back='reset'))
    except ValueError:
        pass

    # Gradient back color.
    print(CLASS().gradient(' ' * maxwidth, name='black', fore='reset'))
    # Explicit gradient fore color.
    print(
        CLASS().gradient('-' * maxwidth, name='white', spread=2, back='blue')
    )
    # Implicit gradient fore color.
    print(CLASS().gradient('_' * maxwidth, name='white'), end='\n\n')


def display_test_gradient_rgb(maxwidth=80):
    """ Test the gradient_rgb method. """
    lines = [
        'This is a block of text made into a gradient, rgb style.'
        for _ in range(10)
    ]
    print(CLASS('\n'.join(lines)).gradient_rgb(
        start=(240, 0, 255),
        stop=(188, 255, 0),
        step=1,
        linemode=True,
        movefactor=-25,
    ))
    linetext = ' This is a block made into a long gradient, rgb style. '
    lines = [
        linetext.center(maxwidth, 'X')
        for _ in range(10)
    ]
    print(CLASS('\n'.join(lines)).gradient_rgb(
        start=(0, 121, 255),
        stop=(191, 0, 182),
        step=1,
        linemode=False,
    ))
    print(CLASS().gradient_rgb(
        ' ' * maxwidth,
        start=(0, 0, 0),
        stop=(255, 255, 255),
        fore='reset',
    ))


def display_test_join(maxwidth=80):
    """ Test join mixed with other methods. """
    def fancy_log(label, msg, tag):
        """ Squeezed justification with complex joins should account for
            existing text width.
        """
        return (
            CLASS(label, fore='green')
            .center(
                # Centering on maxwidth would ruin the next rjust because
                # the spaces created by .center will not be overwritten.
                maxwidth - (len(tag) + 2),
                text=msg,
                fore='yellow',
                squeeze=True
            )
            .rjust(
                maxwidth,
                text=CLASS(tag, fore='red').join(
                    '[', ']',
                    fore='blue'
                ),
                squeeze=True)
        )
    print(fancy_log('This is a label:', 'This is centered.', 'Status: Okay'))

    print(CLASS('|', fore='blue').join(
        'This is regular text.'.ljust(maxwidth // 2 - 1),
        CLASS('This is colored.', fore='red').rjust(maxwidth // 2)
    ))


def display_test_justify(maxwidth=80):
    """ Test the justification methods, alone and mixed with other methods.
    """
    # Justified text should be chainable.
    chunkwidth = maxwidth / 80
    print(
        CLASS()
        .ljust(chunkwidth, text='Left', fore=255, back='green', style='b')
        .center(chunkwidth, text='Middle', fore=255, back='blue', style='b')
        .rjust(chunkwidth, text='Right', fore=255, back='red', style='b')
    )

    # Chained formatting must provide the 'text' argument,
    # otherwise the string is built up and the entire string width grows.
    # This built up string would then be padded, instead of each individual
    # string.
    print(
        CLASS()
        # 256 color methods can be called with bg_<num>, b_<num>, b256_<num>.
        .b_82().b().f_255().ljust(chunkwidth, text='Left')
        .b256_56().b().f_255().center(chunkwidth, text='Middle')
        # Named background color start with 'bg' or 'b_'
        .bgred().b().f_255().rjust(chunkwidth, text='Right')
    )
    # Width should be calculated without color codes.
    print(CLASS('True Middle').center(maxwidth, fore='magenta'))

    # Squeezed justification should account for existing text width.
    # But if text was previously justified, don't ruin it.
    print(CLASS('Lefty', fore=232, back=255).center(
        maxwidth,
        text='Center',
        fore=232,
        back='blue',
        style='bright',
        squeeze=True))
    print(
        CLASS('LeftyCenter'.center(maxwidth // 2), fore=232, back=255)
        .center(
            maxwidth / 2,
            text='Center',
            fore=232,
            back='blue',
            style='bright',
            squeeze=True
        )
    )


def display_test_name_data(width=5, height=20, namewidth=20):
    """ Test known names with name_data. """
    names = list(name_data)
    # Get width * height unique color names and print them (with their color).
    if width * height > len(names):
        width = 5
        height = 10
    names_done = set()
    for _ in range(height):
        cols = []
        for _ in range(width):
            n = random.choice(names)
            while n in names_done:
                n = random.choice(names)
            names_done.add(n)
            cols.append(CLASS(n.center(namewidth), fore=n))
        print(CLASS(' ').join(cols))


def display_test_rainbow(maxwidth=80):
    """ Test rainbow output, with or without linemode (short/long output)
    """
    print(CLASS('This is a rainbow. It is very pretty.').rainbow())
    lines = ['This is a block of text made into a rainbow' for _ in range(5)]
    print(CLASS('\n'.join(lines)).rainbow(movefactor=5))
    lines = [
        'This is a block of text made into a rainbow (rgb mode)'
        for _ in range(5)
    ]
    print(CLASS('\n'.join(lines)).rainbow(movefactor=5, rgb_mode=True))

    lines = ['This is a block made into a long rainbow' for _ in range(5)]
    print(CLASS('\n'.join(lines)).rainbow(linemode=False, rgb_mode=False))
    lines = [
        'This is a block made into a long rainbow (rgb mode)'
        for _ in range(5)
    ]
    print(CLASS('\n'.join(lines)).rainbow(linemode=False, rgb_mode=True))

    # Rainbow should honor fore,back,styles.
    print(CLASS(' ' * maxwidth).rainbow(fore='reset', spread=.5))
    print(CLASS('-' * maxwidth).rainbow(back='black', offset=30))
    print(CLASS(' ' * maxwidth).rainbow(
        fore='reset',
        spread=.5,
        rgb_mode=True
    ))
    print(CLASS('-' * maxwidth).rainbow(
        back='black',
        offset=30,
        rgb_mode=True
    ))

    print(CLASS('Rainbow bright.').rainbow(style='bright').center(maxwidth))


def display_test_rgb(maxwidth=80):
    """ Run through some rgb colors to make sure they will display properly.
    """
    def do_gradient_order(order=('b', 'r', 'g')):
        for r, g, b in gen_rgb_gradient(order=order):
            print(CLASS(' ', back=(r, g, b)), end='')
    do_gradient_order(('b', 'r', 'g'))
    do_gradient_order(('r', 'b', 'g'))
    do_gradient_order(('b', 'g', 'r'))
    do_gradient_order(('g', 'r', 'b'))
    print()
    print(CLASS().rgb(0, 0, 120).b_rgb(150, 0, 0)('This is a test.'))
    print(
        CLASS().rgb(
            255, 55, 55,
            text='Using back/style while setting rgb value.',
            back=(0, 0, 0),
            style='bright')

    )
    print(
        CLASS().b_rgb(
            255, 55, 55,
            text='Using fore/style while setting rgb value.',
            fore=(0, 0, 0),
            style='italic'
        ).white('\nThis should no longer be styled using rgb.')
    )
    print(
        CLASS(
            'One more line, operating on self.data',
            fore=(255, 55, 55),
            back=(0, 0, 0),
        )
        .b_rgb(0, 0, 0)
        .rgb(55, 55, 255, ' and then some.')
    )
    print(
        CLASS('All', 'red', back='white', style='bright')
        .bgwhite().blue(' code')
        .bgwhite().f_135(' types')
        .bgwhite().rgb(25, 20, 155, ' together')
    )
    print(
        CLASS('All', fore='white', back='red')
        .white().bgblue(' back code')
        .white().b_135(' types')
        .white().b_rgb(25, 20, 155, ' together')
    )


def display_test_square_brackets(maxwidth=80):
    """ Test how colr acts when square brackets are mixed with color codes.
    """
    colornames = list(codes['fore'])
    teststrings = (
        (']', '1 bracket'),
        (']' * 20, '20 brackets'),
        ('[bracket test]', ),
        ('[bracket test]', 'this'),
        ('[bracket test]', 'this', '[thing]'),
    )
    for strings in teststrings:
        print(
            CLASS(' ').join(
                CLASS(s, random.choice(colornames))
                for s in strings
            )
        )


def find_tests(pattern):
    """ Find a display_test function by regex. """
    try:
        repat = re.compile(pattern, flags=re.IGNORECASE)
    except re.error as ex:
        raise InvalidArg('Invalid name pattern: {}\n{}'.format(pattern, ex))

    return [
        val
        for name, val in globals().items()
        if (
            name.startswith('display_test_') and
            (repat.search(name) is not None) and
            callable(val)
        )
    ]


def gen_rgb(start=0, stop=255, step=1):
    """ Yields ~(((stop - start) / step) ** 3) rgb values. """
    for r in range(start, stop, step):
        for g in range(start, stop, step):
            for b in range(start, stop, step):
                yield r, g, b


def gen_rgb_gradient(order=('r', 'g', 'b')):
    """ Yields rgb values needed to make a gradient. """
    # This let's the caller select the gradient order by passing an iterable
    # of 'r', 'g', 'b' in the order they need. It could be 'g', 'r', 'b'.
    orderedvalues = {'r': 0, 'g': 0, 'b': 0}
    for i in range(128):
        orderedvalues[order[0]] = 255 - i * 2
        orderedvalues[order[1]] = i * 2
        orderedvalues[order[2]] = 0
        yield orderedvalues['r'], orderedvalues['g'], orderedvalues['b']


def get_terminal_size():
    """ Return terminal (width, height) """
    def ioctl_GWINSZ(fd):
        try:
            import fcntl
            import struct
            import termios
            cr = struct.unpack(
                'hh',
                fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234')
            )
            return cr
        except Exception:
            pass
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except Exception:
            pass
    if not cr:
        try:
            cr = (os.environ['LINES'], os.environ['COLUMNS'])
        except Exception:
            return None
    return int(cr[1]), int(cr[0])


def print_err(*args, **kwargs):
    """ A wrapper for print() that uses stderr by default. """
    if kwargs.get('file', None) is None:
        kwargs['file'] = sys.stderr
    print(*args, **kwargs)


class CustomUserClass(object):
    """ Example user class with a default __colr__ method. """
    def __init__(self, msg='This is a default message.', value=5):
        self.msg = str(msg)
        self.value = value or 5

    def __colr__(self):
        """ Default colr method, when passed to CLASS() with no args. """
        return CLASS(', ').join(
            CLASS(': ').join(
                CLASS('Value', 'cyan'),
                CLASS(self.value, 'blue', style='bright'),
            ),
            CLASS(': ').join(
                CLASS('Message', 'cyan'),
                CLASS(self.msg, 'green', style='underline'),
            ),
        )

    def __str__(self):
        return 'Value: {s.value}, Message: {s.msg}'.format(s=self)


class InvalidArg(ValueError):
    """ Raised when the user has used an invalid argument. """
    def __init__(self, msg=None):
        self.msg = msg or ''

    def __str__(self):
        if self.msg:
            return 'Invalid argument, {}'.format(self.msg)
        return 'Invalid argument!'


if __name__ == '__main__':
    try:
        mainret = main(docopt(USAGESTR, version=VERSIONSTR, script=SCRIPT))
    except InvalidArg as ex:
        print_err(ex)
        mainret = 1
    except (EOFError, KeyboardInterrupt):
        print_err('\nUser cancelled.\n')
        mainret = 2
    except BrokenPipeError:
        print_err('\nBroken pipe, input/output was interrupted.\n')
        mainret = 3
    sys.exit(mainret)
