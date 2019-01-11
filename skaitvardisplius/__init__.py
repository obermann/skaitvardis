#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
This work is in free public domain.
This module is an extesion to module skaitvardis.
It spells numeral together with unit declension, e.g.
7s, 12h, 100$
'''

import re
from skaitvardis import *


# Daiktavardis ė : gervė
INoun3e=Inflection(affrication=(
	set([M.PLURAL, M.GENITIVE]),
	))
INoun3e.FS=[
	u'ė',
	u'ės',
	u'ei',
	u'ę',
	u'e',
	u'ėje',
	u'e'
]
INoun3e.FP=[
	u'ės',
	u'ių',
	u'ėms',
	u'es',
	u'ėmis',
	u'ėse'
]

class Thing:
	def __init__(self, stem, inflection, validDecl=set()):
		self.stem=stem
		self.Inflection=inflection
		self.validDecl=validDecl

minus=[u'minus']
spellEachNumSign=u'!'
things={
	u's': Thing(
		u'sekund',
		INoun3e,
		set([M.FEMININE, M.SINGULAR, M.PLURAL])
		),
	u'min': Thing(
		u'minut',
		INoun3e,
		set([M.FEMININE, M.SINGULAR, M.PLURAL])
		),
	u'h': Thing(
		u'valand',
		INoun1as2a,
		set([M.FEMININE, M.SINGULAR, M.PLURAL])
		),
	u'd': Thing(
		u'dien',
		INoun1as2a,
		set([M.FEMININE, M.SINGULAR, M.PLURAL])
		),
	u'%': Thing(
		u'procent',
		INoun1as2a,
		set([M.MASCULINE, M.SINGULAR, M.PLURAL])
		),
	u'°': Thing(
		u'laipsn',
		INoun1is,
		set([M.MASCULINE, M.SINGULAR, M.PLURAL])
		),
	u'#': Thing(
		u'numer',
		INoun1is,
		set([M.MASCULINE, M.SINGULAR, M.PLURAL])
		),
	u'€': Thing(
		u'eur',
		INoun1as2a,
		set([M.MASCULINE, M.SINGULAR, M.PLURAL])
		),
	u'¢': Thing(
		u'cent',
		INoun1as2a,
		set([M.MASCULINE, M.SINGULAR, M.PLURAL])
		),
	u'$': Thing(
		u'doler',
		INoun1is,
		set([M.MASCULINE, M.SINGULAR, M.PLURAL])
		),
	u'm': Thing(
		u'metr',
		INoun1as2a,
		set([M.MASCULINE, M.SINGULAR, M.PLURAL])
		),
	u'mm': Thing(
		u'milimetr',
		INoun1as2a,
		set([M.MASCULINE, M.SINGULAR, M.PLURAL])
		),
	u'cm': Thing(
		u'centimetr',
		INoun1as2a,
		set([M.MASCULINE, M.SINGULAR, M.PLURAL])
		),
	u'km': Thing(
		u'kilometr',
		INoun1as2a,
		set([M.MASCULINE, M.SINGULAR, M.PLURAL])
		),
	u'ℓ': Thing(
		u'litr',
		INoun1as2a,
		set([M.MASCULINE, M.SINGULAR, M.PLURAL])
		),
}

def spellUnit(x, criterion=set()):
	'''
	Universal method to translate any count of predefined units including fractions to the word list.
	x - number, may be int (long), float or string, e.g. "3/4h", "-0,5%"
	criterion - the set of constants from class M
	'''
	if not isinstance(x, basestring):
		r=minus if x<0 else []
		r.extend(spell(abs(x), criterion))
		return r
	if not x: return [numWord(criterion|set([0]))]
	r=minus if x[0]=='-' else []
	if x[0]=='-' or x[0]=='+':
		x=x[1:]
		if not x: return [numWord(criterion|set([0]))]
	match=re.search('\D+$', x)
	# print x
	# print match.group(0)
	# print [i for i in x]
	# print things.keys()
	if match:
		symbol=match.group(0)
		num=x[0:-len(symbol)]
		if not num:
			return [numWord(criterion|set([0]))]
		elif symbol==spellEachNumSign:
			r=[]
			for c in num.encode():
				try: # toleration
					i=int(c)
				except ValueError:
					continue
				r.append(numWord(criterion|set([i])))
			return r #[numWord(criterion|set([int(i)])) for i in num.encode()]
		elif symbol not in things.keys():
			r.extend(spell(num, criterion)) # tolerate
			return r
	else:
		r.extend(spell(x, criterion))
		return r
	Sym=things[symbol]
	isFraction=re.search('(\d*)\D', num)
	# numi=isFraction.group(1) if isFraction else num
	# if numi=='': numi='0'

	# currate decl
	# default masculine singular
	given=criterion&Sym.validDecl
	gender=given&Gender.toSet()
	number=given&Number.toSet()
	if not gender: gender=Sym.validDecl&Gender.toSet()
	if len(gender)==2: gender=set([M.MASCULINE])
	if not number: number=Sym.validDecl&Number.toSet()
	if len(number)==2: number=set([M.SINGULAR])

	numCriterion=(criterion-AllDecl.toSet())|gender
	symCriterion=numCriterion.copy()

	if M.COLLECTIVE in criterion:
		numCriterion.add(M.SINGULAR)
	else:
		numCriterion|=number

	if isFraction:
		symCriterion-=Case.toSet()
		symCriterion.add(M.GENITIVE)
		if M.SINGULAR in Sym.validDecl:
			symCriterion.add(M.SINGULAR)
		else:
			symCriterion.add(M.PLURAL)
	elif not set([M.ORDINAL, M.DEFINITIVE])&numCriterion:
		if M.SINGULAR not in Sym.validDecl:
			numCriterion-=Group.toSet()
			numCriterion.add(M.NUMERAL)
		# X0 and 1X require genitive!
		if num[-1]=='0' or (len(num)>1 and num[-2]=='1') or M.COLLECTIVE in numCriterion:
			symCriterion-=Case.toSet()
			symCriterion|=(set([M.PLURAL, M.GENITIVE]))
		elif num[-1]=='1' and set([M.CARDINAL, M.TENSDECL])&numCriterion:
			symCriterion.add(M.SINGULAR)
		else:
			symCriterion.add(M.PLURAL)
	else:
		symCriterion|=number

	r.extend(spell(num, numCriterion))
	r.append(Sym.Inflection.declension(Sym.stem, symCriterion))
	return r
	
	
	
	
