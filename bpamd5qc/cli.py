from __future__ import print_function
import sys
from .check import check


def main():
    check(sys.argv[1:])
