"""
Wild Card Match.

A custom implementation of `fnmatch`.

Licensed under MIT
Copyright (c) 2018 Isaac Muse <isaacmuse@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions
of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.
"""
from . import util
from . import _wcparse

__all__ = (
    "CASE", "EXTMATCH", "FORCECASE", "IGNORECASE", "RAWCHARS",
    "NEGATE", "MINUSNEGATE", "DOTMATCH", "BRACE", "SPLIT",
    "NEGATEALL", "FORCEWIN", "FORCEUNIX",
    "C", "F", "I", "R", "N", "M", "D", "E", "S", "B", "A", "W", "U",
    "translate", "fnmatch", "filter", "fnsplit"
)

C = CASE = _wcparse.CASE
F = FORCECASE = _wcparse.FORCECASE
I = IGNORECASE = _wcparse.IGNORECASE
R = RAWCHARS = _wcparse.RAWCHARS
N = NEGATE = _wcparse.NEGATE
M = MINUSNEGATE = _wcparse.MINUSNEGATE
D = DOTMATCH = _wcparse.DOTMATCH
E = EXTMATCH = _wcparse.EXTMATCH
B = BRACE = _wcparse.BRACE
S = SPLIT = _wcparse.SPLIT
A = NEGATEALL = _wcparse.NEGATEALL
W = FORCEWIN = _wcparse.FORCEWIN
U = FORCEUNIX = _wcparse.FORCEUNIX

FLAG_MASK = (
    CASE |
    FORCECASE |
    IGNORECASE |
    RAWCHARS |
    NEGATE |
    MINUSNEGATE |
    DOTMATCH |
    EXTMATCH |
    BRACE |
    SPLIT |
    NEGATEALL |
    FORCEWIN |
    FORCEUNIX
)


def _flag_transform(flags):
    """Transform flags to glob defaults."""

    _wcparse.deprecate_flags(flags)

    # Enabling both cancels out
    if flags & _wcparse.FORCEUNIX and flags & _wcparse.FORCEWIN:
        flags ^= _wcparse.FORCEWIN | _wcparse.FORCEUNIX

    # Force ignore case if Windows
    if flags & _wcparse.FORCEWIN and flags & _wcparse.FORCECASE:
        flags ^= _wcparse.FORCECASE

    return (flags & FLAG_MASK)


@util.deprecated("Use the 'SPLIT' flag instead.")
def fnsplit(pattern, *, flags=0):
    """Split pattern by '|'."""

    return _wcparse.WcSplit(pattern, _flag_transform(flags)).split()


def translate(patterns, *, flags=0):
    """Translate `fnmatch` pattern."""

    flags = _flag_transform(flags)
    return _wcparse.translate(_wcparse.split(patterns, flags), flags)


def fnmatch(filename, patterns, *, flags=0):
    """
    Check if filename matches pattern.

    By default case sensitivity is determined by the file system,
    but if `case_sensitive` is set, respect that instead.
    """

    flags = _flag_transform(flags)
    if not _wcparse.is_unix_style(flags):
        filename = _wcparse.norm_slash(filename, flags)
    return _wcparse.compile(_wcparse.split(patterns, flags), flags).match(filename)


def filter(filenames, patterns, *, flags=0):  # noqa A001
    """Filter names using pattern."""

    matches = []

    flags = _flag_transform(flags)
    unix = _wcparse.is_unix_style(flags)
    obj = _wcparse.compile(_wcparse.split(patterns, flags), flags)

    for filename in filenames:
        if not unix:
            filename = _wcparse.norm_slash(filename, flags)
        if obj.match(filename):
            matches.append(filename)
    return matches
