#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
This work is in free public domain.
Skaitvardis is Lithuanian for numeral.
This module spells positive integers, decimal and rational fractions in Lithuanian.
You may indicate the group (cardinals vs. numerals), gender, number and case of the counted target.
http://www.šaltiniai.info/index/details/578
'''
def rang(x,y,step=1):
	return list(range(x,y+1,step)) # list() for Python 3
def rset(x,y,step=1):
	return set(rang(x,y,step))
def rsetz(x,zeroes,times):
	return set([x]+[10**(zeroes*i)*x for i in rang(1,times)])

# Kiekiniai-pargrindiniai
stemsBasic={
	0: u'nul',
	1: u'vien',
	2: u'du',
	3: u'trys',
	4: u'ketur',
	5: u'penk',
	6: u'šeš',
	7: u'septyn',
	8: u'aštuon',
	9: u'devyn',
	10: u'dešimt',
	11: u'vienuolik',
	12: u'dvylik',
	13: u'trylik',
	14: u'keturiolik',
	15: u'penkiolik',
	16: u'šešiolik',
	17: u'septyniolik',
	18: u'aštuoniolik',
	19: u'devyniolik',
	20: u'dvidešimt', # 20..90=accusative+10
	30: u'trisdešimt',
	40: u'keturiasdešimt',
	50: u'penkiasdešimt',
	60: u'šešiasdešimt',
	70: u'septyniasdešimt',
	80: u'aštuoniasdešimt',
	90: u'devyniasdešimt',
	100: u'šimt',
	1000: u'tūkstant',
	1000000: u'milijon',
	1000000000: u'milijard',
	1000000000000: u'trilijon',
	1000000000000000: u'kvadrilijon',
	1000000000000000000: u'kvintilijon',
	1000000000000000000000: u'sikstilijon',
	1000000000000000000000000: u'septilijon',}

# Dauginiai
stemsNumeral={
	2: u'dvej',
	3: u'trej',
	4: u'ketver',}
stemsNumeral.update(dict([(k,stemsBasic[k]+u'er') for k in [1]+rang(5,9)]))

# Kuopiniai
stemsCollective=dict([(k,stemsNumeral[k]+u'et') for k in [2,3]])
stemsCollective[4]=u'ketvet'
stemsCollective.update(dict([(k,stemsBasic[k]+u'et') for k in [1]+rang(5,9)]))

# Kelintiniai
stemsOrdinal={
	1: u'pirm',
	2: u'antr',
	3: u'treči',
	4: u'ketvirt',
	7: u'septint',
	8: u'aštunt',
	9: u'devint',}
stemsOrdinal.update(dict([(k,stemsBasic[k]+u't') for k in [5,6]+rang(11,19)]))

# https://docs.python.org/2/tutorial/classes.html
# https://realpython.com/instance-class-and-static-methods-demystified/
class ConstantLister(object):
	'''
	Enabling constants classification.
	'''
	@classmethod
	def toList(cls):
		return [v for c in cls.__mro__ if c is not object for k,v in c.__dict__.items() if isinstance(v,(int,long))]
	@classmethod
	def toSet(cls):
		return set(cls.toList())
	@classmethod
	def getName(cls,value):
		for c in cls.__mro__: 
			if c is not object: 
				for k,v in c.__dict__.items(): 
					if isinstance(v,(int,long)) and v==value:
						return k
		# for k in dir(cls):
			# if k[0]!='_' and getattr(cls, k)==value: 
				# return k

# Constants
class Group(ConstantLister):
	'''
	TENSDECL is the same as CARDINAL except the case will be applied to X0 numeral when it is the last word (e.g. 140 vs. 142).
	This is not strictly standard, but widely spoken.
	The last word restriction can be defended only on the grouds 
	that no big number (with more than one X0) never spoken widely (e.g. 350910).
	'''
	CARDINAL=-1
	TENSDECL=-2
	NUMERAL=-4
	COLLECTIVE=-5
	ORDINAL=-6
	DEFINITIVE=-7
	STEMONLY=-9
class Gender(ConstantLister):
	MASCULINE=-10
	FEMININE=-11
class Number(ConstantLister):
	SINGULAR=-100
	PLURAL=-111
class AllDecl(Gender, Number):
	pass
class Case(ConstantLister):	
	NOMINATIVE=-1000
	GENITIVE=-1001
	DATIVE=-1002
	ACCUSATIVE=-1003
	INSTRUMENTATIVE=-1004
	LOCATIVE=-1005
	VOCATIVE=-1006
class M(Group, Gender, Number, Case, ConstantLister):
	'''
	All constants available under short record name M.
	WRITEONES - use to require "one" before hundred, thousand.
	This is non-standard, but maybe some paranoid documents (financial) may use it.
	'''
	WRITEONES=-200

class Inflection:
	_ms=set([M.MASCULINE, M.SINGULAR])
	_mp=set([M.MASCULINE, M.PLURAL])
	_fs=set([M.FEMININE, M.SINGULAR])
	_fp=set([M.FEMININE, M.PLURAL])
	
	def __init__(self, endingOnly=True, affrication=None):
		self.MS=None
		self.MP=None
		self.FS=None
		self.FP=None
		self.endingOnly=endingOnly
		self.affrication=affrication
	
	@staticmethod
	def caseIndex(constant):
		return abs(constant)-1000
		
	def declension(self, stem, criterion):
		if criterion>=self._ms: x=self.MS
		elif criterion>=self._mp: x=self.MP
		elif criterion>=self._fs: x=self.FS
		elif criterion>=self._fp: x=self.FP
		else:
			return stem
		# vocative=nominative by default
		if len(x)==6: x.append(x[0]) 
		# Case
		case=criterion&Case.toSet()
		if case:
			for c in case: break
		else:
			c=M.NOMINATIVE
		c=self.caseIndex(c)
		# Synth
		if not self.endingOnly: return x[c]
		if self.affrication is not None:
			if stem[-1:]=='t':
				for a in self.affrication:
					if a<=criterion:
						return stem[0:-1]+u'č'+x[c]
			elif stem[-1:]=='d':
				for a in self.affrication:
					if a<=criterion:
						return stem+u'ž'+x[c]
		return stem+x[c]
	

INoun1as2a=Inflection()
# Daiktavardis a : vyras vyro vyrui
INoun1as2a.MS=[
	u'as',
	u'o',
	u'ui',
	u'ą',
	u'u',
	u'e',
	u'e'
]
INoun1as2a.MP=[
	u'ai',
	u'ų',
	u'ams',
	u'us',
	u'ais',
	u'uose'
]
# Daiktavardis o : šaka
INoun1as2a.FS=[
	u'a',
	u'os',
	u'ai',
	u'ą', # !vienuolika
	u'a',
	u'oje'
]
INoun1as2a.FP=[
	u'os',
	u'ų',
	u'oms',
	u'as',
	u'omis',
	u'ose'
]

# Daiktavardis a : nulis
INoun1is=Inflection(affrication=(
	set([M.PLURAL]), 
	set([M.GENITIVE]), 
	set([M.DATIVE]), 
	set([M.INSTRUMENTATIVE])
	))
INoun1is.MS=[
	u'is',
	u'io',
	u'iui',
	u'į',
	u'iu',
	u'yje',
	u'i'
]
INoun1is.MP=[u'i'+x for x in INoun1as2a.MP]

# Daiktavardis i : avis
# http://www.vlkk.lt/konsultacijos/9577-desimtys-desimties-desimties-kirciavimas
INoun5is=Inflection(affrication=(
	set([M.SINGULAR, M.DATIVE]), 
	set([M.SINGULAR, M.INSTRUMENTATIVE]), 
	set([M.PLURAL, M.GENITIVE])
	))
INoun5is.FS=[
	u'is',
	u'ies',
	u'iai',
	u'į',
	u'ia', # -imi
	u'yje',
	u'ie'
]
INoun5is.FP=[
	u'ys',
	u'ių',
	u'ims',
	u'is',
	u'imis',
	u'yse'
]

# Būdvardis a : geras gera
IAdj1as=Inflection()
IAdj1as.MS=[
	u'as',
	u'o',
	u'am',
	u'ą',
	u'u',
	u'ame'
]
IAdj1as.MP=[
	u'i',
	u'ų',
	u'iems',
	u'us',
	u'ais',
	u'uose'
]
IAdj1as.FS=INoun1as2a.FS
IAdj1as.FP=INoun1as2a.FP

# Būdvardis ia : žali žalios
IAdj1ias=Inflection()
IAdj1ias.MP=[x if x[0]==u'i' else u'i'+x for x in IAdj1as.MP]
IAdj1ias.FP=[u'i'+x for x in IAdj1as.FP]

# Įvardžiuotinis būdvardis
IAdjDef=Inflection()
IAdjDef.MS=[
	u'asis',
	u'ojo',
	u'ajam',
	u'ąjį',
	u'uoju',
	u'ajame'
]
IAdjDef.MP=[
	u'ieji',
	u'ųjų',
	u'iesiems',
	u'uosius',
	u'aisiais',
	u'uosiuose'
]
IAdjDef.FS=[
	u'oji',
	u'osios',
	u'ajai',
	u'ąją',
	u'ąja',
	u'ojoje'
]
IAdjDef.FP=[
	u'osios',
	u'ųjų',
	u'osioms',
	u'ąsias',
	u'osiomis',
	u'osiose'
]

# Išimtys

ISpec2=Inflection(endingOnly=False)
ISpec2.MP=[
	u'du',
	u'dviejų',
	u'dviem',
	u'du',
	u'dviem',
	u'dviejuose'
]
ISpec2.FP=[
	u'dvi',
	u'dviejų',
	u'dviem',
	u'dvi',
	u'dviem',
	u'dviejose'
]

ISpec3=Inflection(endingOnly=False)
ISpec3.MP=[
	u'trys',
	u'trijų',
	u'trims',
	u'tris',
	u'trimis',
	u'trijuose'
]
ISpec3.FP=ISpec3.MP[:]
ISpec3.FP[ISpec3.caseIndex(M.LOCATIVE)]=u'trijose'

# http://www.vlkk.lt/konsultacijos/7421-dauginiu-skaitvardziu-linksniavimas
ISpecX=Inflection()
ISpecX.MP=IAdj1ias.MP[:]
ISpecX.MP[ISpecX.caseIndex(M.ACCUSATIVE)]=u'is'
ISpecX.FP=IAdj1ias.FP

# http://www.vlkk.lt/konsultacijos/2770-sudurtiniai-skaitvardziai-linksniavimas
ISpec1X=Inflection()
ISpec1X.FS=INoun1as2a.FS[:]
ISpec1X.FS[ISpec1X.caseIndex(M.ACCUSATIVE)]=u'a'

ISpecX0=Inflection(affrication=INoun5is.affrication)
ISpecX0.FS=INoun5is.FS[:]
ISpecX0.FS[ISpecX0.caseIndex(M.NOMINATIVE)]=u''
ISpecX0.FS[ISpecX0.caseIndex(M.ACCUSATIVE)]=u''


class Num:
	'''
	Class for lexical database records.
	'''
	def __init__(self, criterion, inflection, validDecl=set(), stems=None):
		self.criterion=criterion
		self.Inflection=inflection
		self.validDecl=validDecl
		self.stems=stems
	def declension(self, criterion):
		stem=None
		if self.stems:
			for i in criterion:
				if i >= 0:
					stem=self.stems[i]
					break
		if len(self.validDecl)<3:
			return self.Inflection.declension(stem, (criterion-AllDecl.toSet())|self.validDecl)
		else:
			# currate decl
			# default masculine singular
			given=criterion&self.validDecl
			gender=given&Gender.toSet()
			number=given&Number.toSet()
			if not gender: gender=self.validDecl&Gender.toSet()
			if len(gender)==2: gender=set([M.MASCULINE])
			if not number: number=self.validDecl&Number.toSet()
			if len(number)==2: number=set([M.SINGULAR])
			return self.Inflection.declension(stem, (criterion-AllDecl.toSet())|gender|number)
			
db=(

	Num(set([
	M.STEMONLY])
	| set(stemsBasic.keys())-rset(1,9)-rset(11,19),
	Inflection(), set(),
	stemsBasic),
	
	Num(set([
	M.STEMONLY])
	| rset(1,9) | rset(11,19),
	Inflection(), set(),
	stemsOrdinal),
	
	Num(set([
	M.CARDINAL, 
	M.TENSDECL,
	M.NUMERAL,
	M.COLLECTIVE,
	M.ORDINAL, M.DEFINITIVE, # xtreme toleration
	0]),
	INoun1is, set([M.MASCULINE, M.SINGULAR]),
	stemsBasic),
	
	Num(set([
	M.CARDINAL, 
	M.TENSDECL,
	1]),
	IAdj1as, set([M.MASCULINE, M.FEMININE, M.SINGULAR]),
	stemsBasic),
	
	Num(set([
	M.CARDINAL, 
	M.TENSDECL,
	2]),
	ISpec2, set([M.MASCULINE, M.FEMININE, M.PLURAL]),
	),
	
	Num(set([
	M.CARDINAL, 
	M.TENSDECL,
	3]),
	ISpec3, set([M.MASCULINE, M.FEMININE, M.PLURAL]),
	),
	
	Num(set([
	M.CARDINAL,
	M.TENSDECL]) 
	| rset(4,9),
	ISpecX, set([M.MASCULINE, M.FEMININE, M.PLURAL]),
	stemsBasic),
	
	Num(set([
	M.CARDINAL,
	M.TENSDECL, 
	M.NUMERAL,
	M.COLLECTIVE])
	| rset(11,19),
	ISpec1X, set([M.FEMININE, M.SINGULAR]),
	stemsBasic),
	
	Num(set([
	M.CARDINAL, 
	M.NUMERAL])
	| rset(10,90,10),
	Inflection(), set(),
	stemsBasic),

	Num(set([
	M.CARDINAL,
	M.TENSDECL, 
	M.NUMERAL,
	M.COLLECTIVE,
	100]) | rsetz(1000000,3,6),
	INoun1as2a, set([M.MASCULINE, M.SINGULAR, M.PLURAL]),
	stemsBasic),
	
	Num(set([
	M.CARDINAL,
	M.TENSDECL, 
	M.NUMERAL,
	M.COLLECTIVE,
	1000]),
	INoun1is, set([M.MASCULINE, M.SINGULAR, M.PLURAL]),
	stemsBasic),
		
	Num(set([
	M.TENSDECL])
	| rset(10,90,10),
	ISpecX0, set([M.FEMININE, M.SINGULAR]),
	stemsBasic),
	
	Num(set([
	M.NUMERAL,
	1]) | rset(4,9),
	IAdj1ias, set([M.MASCULINE, M.FEMININE, M.PLURAL]),
	stemsNumeral),
	
	Num(set([
	M.NUMERAL,
	2, 3]),
	IAdj1as, set([M.MASCULINE, M.FEMININE, M.PLURAL]),
	stemsNumeral),
	
	Num(set([
	M.COLLECTIVE])
	| rset(1,9),
	INoun1as2a, set([M.MASCULINE, M.SINGULAR, M.PLURAL]),
	stemsCollective),
		
	Num(set([
	M.COLLECTIVE, # by standard it is basic cardinal, but I found place and likely use for it as collective
	10]),
	INoun5is, set([M.FEMININE, M.SINGULAR, M.PLURAL]),
	stemsBasic),
	
	Num(set([
	M.COLLECTIVE])
	| rset(20,90,10),
	Inflection(), set(), # tempting to mimic 10, but it definitely is going too far
	stemsBasic),
	
	Num(set([
	M.ORDINAL])
	| rset(1,9) | rset(11,19),
	IAdj1as, AllDecl.toSet(),
	stemsOrdinal),
	
	Num(set([
	M.ORDINAL,
	1000]) | rset(10,90,10),
	IAdj1as, AllDecl.toSet(),
	stemsBasic),
	
	Num(set([
	M.DEFINITIVE])
	| rset(1,9) | rset(11,19),
	IAdjDef, AllDecl.toSet(),
	stemsOrdinal),
	
	Num(set([
	M.DEFINITIVE,
	1000]) | rset(10,90,10),
	IAdjDef, AllDecl.toSet(),
	stemsBasic),
	
	Num(set([
	M.ORDINAL, 
	M.DEFINITIVE,
	100]) | rsetz(1000000,3,6), # always DEFINITIVE
	IAdjDef, AllDecl.toSet(),
	stemsBasic),
	
)

def numWord(criterion):
	'''
	Translate known to be one word integer number to one word.
	Here lexical database is consumed.
	criterion - the set of constants from class M with integer to be translated included
	'''
	simpleCriterion=criterion-Case.toSet()-AllDecl.toSet() # tolerate any decl.
	for num in db:
		if simpleCriterion<=num.criterion:
			return num.declension(criterion)
	return None

def spellInt(criterion):
	'''
	Main method to translate any positive integer number to the word list.
	criterion - the set of constants from class M with integer to be translated included
	'''
	# put number to i
	i=0
	for i in criterion:
		if i==0:
			return [numWord(criterion)]
		elif i>0:
			criterion.discard(i)
			break
	if i<=0: return [numWord(criterion|set([0]))] # tolerate
	if not Group.toSet()&criterion: criterion.add(M.CARDINAL)
	# there are no collective above 10
	elif M.COLLECTIVE in criterion and i>10:
		criterion.discard(M.COLLECTIVE)
		criterion.add(M.CARDINAL) # default, maybe M.TENSDECL
	localCriterion=set([M.CARDINAL])
	if not set([M.ORDINAL, M.DEFINITIVE])&criterion: # standard test for ordinals vs. cardinals
		localCriterion|=criterion&Case.toSet()
	# accumulating in line[] in reverse order: 501 -> 1,100,5
	# then bool(line)==False means working with the last word
	# only it could be other than cardinal, have actual gender & number
	# most words in cardinal have actual case and only the last in ordinal 
	line=[]
	e=-1
	while i:
		# looping triplets: 23.000.456.789
		# i99=1..99; i90=1..9 of 10; etc.
		i,i999=divmod(i,1000)
		e+=1
		if i999==0: continue # got x1000
		i900,i99=divmod(i999,100)
		i90,i9=divmod(i99,10)
		# triplet position x1000
		if e:
			if line or not set([M.ORDINAL, M.DEFINITIVE])&criterion:
				if i9==1: line.append(set([1000**e, M.SINGULAR])|localCriterion)
				# X0 and 1X require genitive!
				elif i9==0 or i99 in range(11,20): line.append(set([1000**e, M.PLURAL, M.GENITIVE])|(localCriterion-Case.toSet()))
				else: line.append(set([1000**e, M.PLURAL])|localCriterion)
			else: line.append(set([1000**e])|criterion)
		if i999==1 and line and M.WRITEONES not in criterion: continue
		if i99:
			if i99 in range(10,20): line.append(set([i99])|(localCriterion if line else criterion))
			else:
				if i9: line.append(set([i9])|(localCriterion if line else criterion))
				if i90: line.append(set([i90*10])|(localCriterion if line else criterion))
		if i900:
			if line or not set([M.ORDINAL, M.DEFINITIVE])&criterion:
				if i900==1: line.append(set([100, M.SINGULAR])|localCriterion)
				else: line.append(set([100, M.PLURAL])|localCriterion)
			else: line.append(set([100])|criterion)
			if i900>1 or M.WRITEONES in criterion:
				line.append(set([i900])|localCriterion)	
	#print [m for n in reversed(line) for m in n if m>0]
	#print line[::-1]
	return [numWord(n) for n in reversed(line)]

def spellFloat(criterion):
	'''
	Main method to translate any positive float number to the word list.
	criterion - the set of constants from class M with float to be translated included
	'''
	# put number to x
	x=0
	for x in criterion:
		if x==0:
			return [numWord(criterion|set([0]))]
		elif x>0:
			criterion.discard(x)
			break
	if x<=0: return [numWord(criterion|set([0]))] # tolerate
	istr,fstr=str(x).split('.')
	i=long(istr)
	f=long(fstr)
	e=10**len(fstr)
	r=spellInt(set([i])|criterion)
	if i==0: r.append(u'sveikų')
	if f:
		r.append(u'ir')
		r.extend(spellInt(set([f, M.FEMININE])|(Case.toSet()&criterion)))
		r.extend(spellInt(set([e, M.DEFINITIVE, M.FEMININE, M.SINGULAR if fstr[-1]=='1' else M.PLURAL])|(Case.toSet()&criterion)))
	return r

def spell(x, criterion=set()):
	'''
	Universal method to translate any positive number including fractions to the word list.
	x - number, may be int (long), float or string, e.g. "3/4"
	criterion - the set of constants from class M
	'''
	if isinstance(x, (int, long)): return spellInt(set([x])|criterion)
	if isinstance(x, float): return spellFloat(set([x])|criterion)
	if isinstance(x, basestring):
		if ',' in x: x=x.replace(',','.')
		if '.' in x: return spellFloat(set([float(x)])|criterion)
		if '/' in x:
			istr,fstr=str(x).split('/')
			i=long(istr)
			f=long(fstr)
			r=spellInt(set([i, M.FEMININE])|(criterion-Gender.toSet()))
			r.extend(spellInt(set([f, M.DEFINITIVE, M.FEMININE, M.SINGULAR if i==1 else M.PLURAL])|(Case.toSet()&criterion)))
			return r
		return spellInt(set([long(x)])|criterion)
