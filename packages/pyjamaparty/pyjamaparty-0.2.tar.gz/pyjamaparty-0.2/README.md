[![PyPI version](https://badge.fury.io/py/pyjamaparty.svg)](https://badge.fury.io/py/pyjamaparty)   [![Build Status](https://travis-ci.org/krajasek/pyjamaparty.svg?branch=master)](https://travis-ci.org/krajasek/pyjamaparty)

# pyjamaparty
Set of casual python utilities

## Mutable String Builder
```python
from pyjamaparty.strutils import string_builder as sb
s = sb.StringBuilder()

s.append('Wow, ')
s.append('such a nice ').append('builder')
print(len(s))

s += ' :)'

s[:3] = 'whee'

s.remove(1)

for c in s:
    pass

print(str(s))
```
