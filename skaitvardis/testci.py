#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import sys, path

if __name__ == '__main__' and __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from skaitvardis import *

if len(sys.argv)==2:
	for p in (spell(sys.argv[1], set([M.TENSDECL, M.INSTRUMENTATIVE]))): print p

	