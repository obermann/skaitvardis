# skaitvardis
Python modules for spelling any number in Lithuanian.

**skaitvardis** - is a core speller.
Skaitvardis is Lithuanian for numeral.
This module spells positive integers, decimal and rational fractions in Lithuanian.
You may indicate the group (cardinals vs. numerals), gender, number and case of the counted target.

**skaitvardisplius** - is an extension to module skaitvardis.
It spells a numeral together with unit declension, e.g.
7s, 12h, 100$

May be useful for TTS (Text To Speach) or document processing.

## Example
```python
import win_unicode_console
win_unicode_console.enable(use_unicode_argv=True)

from skaitvardisplius import *

if len(sys.argv)==2:
	for p in (spellUnit(sys.argv[1], set([M.TENSDECL, M.INSTRUMENTATIVE]))): print p
```

## Compatibility
Python 2.6 and 3

## Resources
http://www.šaltiniai.info/index/details/578

## Notes
I wanted to use it with Python 2.6 and that made using sets look ugly, sorry.

I am a native speaker of Lithuanian, but not a linguist.
