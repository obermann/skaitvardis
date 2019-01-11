#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import sys, path

if __name__ == '__main__' and __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from skaitvardis import *

# http://wiki.python.org/moin/PrintFails
import codecs; 
sys.stdout=codecs.getwriter('utf8')(sys.stdout)
sys.stderr=codecs.getwriter('utf8')(sys.stderr)

def testNumWord():
	n=rang(1,9)
	n.extend(rang(11,19))
	n.extend(rang(10,90,10))
	n.append(0)
	n.append(100)
	n.extend(sorted(rsetz(1000,3,7)))

	d=[set([a,b]) for a in sorted(Gender.toList(),  reverse=True) for b in sorted(Number.toList(),  reverse=True)]
	
	result=[set([i,ii,iiii])|iii for i in sorted(Group.toList(), reverse=True) for ii in n for iii in d for iiii in sorted(Case.toList(), reverse=True)]
	
	print('<html><head>')
	print('<link rel="stylesheet" href="testnumword.css"/>')
	print('</head><body>')
	
	for i in result:
		if set([1, M.MASCULINE, M.SINGULAR, M.NOMINATIVE]) <= i:
			print('</tr></table>')
			print('<p><b>')
			#print(i)
			for p in i-set([1])-Case.toSet()-AllDecl.toSet(): print(M.getName(p)+' ')
			print('</b></p>')
			print('<table><tr><th>&nbsp;</th><th>&nbsp;</th>')
			for p in [Case.getName(n) for n in sorted(Case.toList(), reverse=True)]: print('<th>'+p+'</th>')
		if M.NOMINATIVE in i:
			print('</tr>')
			print('<tr>')
			#print('<th>&nbsp;</th>')
			print('<th>'+Gender.getName(list(Gender.toSet()&i)[0])+'&nbsp;'+Number.getName(list(Number.toSet()&i)[0])+'</th>')
			for p in i: 
				if p>=0:
					if p>100: p='{0:.0e}'.format(p)
					else: p=str(p) 
					break
			print('<th style="white-space:nowrap;text-align:right;">'+p+'</th>')
		print('<td>')
		print(numWord(i))
		print('</td>')
		
	print('</body></html>')

testNumWord()
