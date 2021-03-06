pluckit
======
Extract values from collection items.


### Install
```pip install pluckit```


### Usage
```python
from pluckit import pluck

data = [
  {'x': 1, 'y': 2},
  {'x': 2, 'y': 4},
  {'x': 3, 'y': 6},
]
pluck(data, 'x')
> [1, 2, 3]


# supports arbitrarily deep plucks and function calls
people = [
    { 'name': 'Daniel', 'friends': [ 'Josh', 'Mel' ] },
    { 'name': 'Mel', 'friends': [ 'Daniel', 'Suzy' ] },
]
pluck(people, 'friends[-1].lower[:3]')
> [ 'mel', 'suz' ]



# use Pluckables for built-in functionality

from pluckit.pluckable import PluckableList

PluckableList([
  {'x': 1, 'y': 2},
  {'x': 2, 'y': 4},
  {'x': 3, 'y': 6},
]).pluck('x')
> [1, 2, 3]


# use the Pluckable mixin to build your own

from pluckit import Pluckable
class MyDict(dict, Pluckable): pass

MyDict({
  'home' : {'x' : 1, 'y' : 2},
  'work' : {'x' : 3, 'y' : 6},
}).pluck('x')
> {'home' : 1, 'work' : 3}
```

----
[![Build Status](https://travis-ci.org/dpep/py_pluckit.svg?branch=master)](https://travis-ci.org/dpep/py_pluckit)
[![Coverage Status](https://coveralls.io/repos/github/dpep/py_pluckit/badge.svg?branch=master)](https://coveralls.io/github/dpep/py_pluckit?branch=master)
[![installs](https://img.shields.io/pypi/dm/pluckit.svg?label=installs)](https://pypi.org/project/pluckit)
