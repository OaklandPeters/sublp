"""
Commandline interface.
"""
from __future__ import absolute_import
import sys

from sublp import Sublp

if __name__ == "__main__":
    Sublp(sys.argv[1])
