#!/usr/bin/env python3

from __future__ import print_function
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


def check_md5(md5_fname):
    basedir = os.path.dirname(md5_fname)
    missing = []
    in_md5 = set()
    with open(md5_fname) as fd:
        for md5, path in md5lines(fd):
            in_md5.add(path)
            if path == 'TestFiles.exe':
                continue
            if not os.access(os.path.join(basedir, path), os.R_OK):
                missing.append(path)
    extra = []
    for fname in os.listdir(basedir):
        if fname in in_md5:
            continue
        if fname.endswith('.md5.log') or fname.endswith('.md5') or fname.endswith('_checksums.txt') or fname.endswith('_checksums.txt.log'):
            continue
        if fname.endswith('.xlsx'):
            continue
        extra.append(fname)
    if missing or extra:
        print('## %s' % (os.path.abspath(basedir)))
        print()
        print('Errors for MD5 file: %s' % (os.path.basename(md5_fname)))
        print()
    if missing:
        print('### missing files')
        print()
        for path in sorted(missing):
            print(' - %s' % path)
        print()
    if extra:
        print('### extra files')
        print()
        for path in sorted(extra):
            print(' - %s' % path)
        print()
    return not (missing or extra)


def check(files):
    n_pass = 0
    n_fail = 0
    for md5_file in files:
        if not check_md5(md5_file):
            n_fail += 1
        else:
            n_pass += 1
    print()
    print("## Run summary: pass=%d fail=%d" % (n_pass, n_fail))
