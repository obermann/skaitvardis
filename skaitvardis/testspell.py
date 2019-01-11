#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import sys, path

if __name__ == '__main__' and __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import random
from skaitvardis import *

# https://chase-seibert.github.io/blog/2014/01/12/python-unicode-console-output.html
# http://wiki.python.org/moin/PrintFails
# import codecs, locale; 
# sys.stdout=codecs.getwriter('utf8')(sys.stdout)
# sys.stderr=codecs.getwriter('utf8')(sys.stderr)
# sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout);

def testSpell():
	a=[0,1,2,3,random.randrange(5,10)]
	random.shuffle(a)
	b=[]
	for n in range(5):
		b.append([0,1,random.randrange(2,10)])
		random.shuffle(b[n])
	c=[1,random.randrange(2,1000)]
	random.shuffle(c)
	
	r=[str(cc)+str(b0)+str(b1)+str(b2)+str(b3)+str(b4)+str(aa )
		for cc in c for b4 in b[4] for b3 in b[3] for b2 in b[2] for b1 in b[1] for b0 in b[0] for aa in a]
	
	print r
	
testSpell()