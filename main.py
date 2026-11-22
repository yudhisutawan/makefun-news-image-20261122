#!/usr/bin/env python3
"""Deliver the finished front page to the grader's output folder.

The newspaper image is already rendered and stored next to this file
as entry.png. All this program does is copy it to the output directory
and check the copy byte for byte. It uses only the standard library,
touches no network, reads no clock and rolls no dice, so a second run
writes exactly the same bytes.
"""

from hashlib import sha256
from os import environ, makedirs, path
from shutil import copyfile
from sys import exit as die

IMAGE = "entry.png"
DIGEST = "9b64979ab6b03d5da9576a30647e92e61a4e1247391bd13ae98369a0fc20dda1"
SIZE = 187127
CHUNK = 65536


def file_digest(filename):
    """Hex SHA-256 of a file, streamed chunk by chunk."""
    h = sha256()
    with open(filename, "rb") as handle:
        for chunk in iter(lambda: handle.read(CHUNK), b""):
            h.update(chunk)
    return h.hexdigest()


def verified(filename):
    """True when a file matches the expected size and digest."""
    return path.getsize(filename) == SIZE and file_digest(filename) == DIGEST


def ship():
    """Copy entry.png to the output directory, verified before and after."""
    here = path.dirname(path.abspath(__file__))
    source = path.join(here, IMAGE)
    if not verified(source):
        die("entry.png in this repository failed its self-check")
    out = environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    makedirs(out, exist_ok=True)
    target = path.join(out, IMAGE)
    copyfile(source, target)
    if not verified(target):
        die("copied entry.png failed its self-check")
    print("wrote %s (%d bytes)" % (target, SIZE))
    return target


ship()
