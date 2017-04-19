#!/usr/bin/env python3

from __future__ import print_function
from collections import defaultdict
import re
import os

bsd_md5_re = re.compile(r'^MD5 \(([^\)]+)\) = ([0-9a-f]{32})$')
linux_md5_re = re.compile(r'^([0-9a-f]{32}) [\* ](.*)$')


def md5lines(fd):
    "read MD5 lines from `fd` and yield pairs of (md5, path)"
    for line in fd:
        line = line.strip()
        # skip blank lines
        if line == '':
            continue
        m = bsd_md5_re.match(line)
        if m:
            path, md5 = m.groups()
            yield md5, path
            continue
        m = linux_md5_re.match(line)
        if m:
            md5, path = m.groups()
            yield md5, path
            continue
        raise Exception("Could not parse MD5 line: %s" % line)


def check_md5(md5_fname, all_md5_paths):
    basedir = os.path.dirname(md5_fname)
    missing = []
    with open(md5_fname) as fd:
        for md5, path in md5lines(fd):
            all_md5_paths.add(path)
            if path == 'TestFiles.exe':
                continue
            if not os.access(os.path.join(basedir, path), os.R_OK):
                missing.append(path)
    return missing


def check_dir(basedir, files):
    all_md5_paths = set()
    md5_missing = {}
    for md5_file in files:
        missing = check_md5(md5_file, all_md5_paths)
        if missing:
            md5_missing[md5_file] = missing

    extra = []
    for root, dirs, files in os.walk(basedir):
        for fname in (os.path.relpath(t, basedir) for t in files):
            if fname in all_md5_paths:
                continue
            if fname.endswith('.md5.log') or fname.endswith('.md5') or fname.endswith('_checksums.txt') or fname.endswith('_checksums.txt.log'):
                continue
            if fname.endswith('.xlsx'):
                continue
            extra.append(fname)

    if not md5_missing and not extra:
        # no problems found
        return

    print('## %s' % (basedir))

    for md5_file, missing in md5_missing.items():
        print()
        print('### MD5 references non-existant files: %s' % (os.path.basename(md5_file)))
        print()
        for path in sorted(missing):
            print(' - %s' % path)
        print()

    if extra:
        print('### Files under directory not checksummed')
        print()
        for path in sorted(extra):
            print(' - %s' % path)
        print()


def check(files):
    # group MD5 files by their base directory
    bydir = defaultdict(list)
    for md5_file in files:
        bydir[os.path.dirname(md5_file)].append(md5_file)

    for basedir, dir_files in bydir.items():
        check_dir(basedir, dir_files)
