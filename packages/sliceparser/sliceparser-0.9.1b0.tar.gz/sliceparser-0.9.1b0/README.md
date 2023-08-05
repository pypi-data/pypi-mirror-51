sliceparser
===========


Introduction
------------

As per [this question](https://stackoverflow.com/q/680826/7881370), creating from string slice object, or even advanced indexing tuple, is a common requirement.
However, there exists few robust and safe solution, if at all, to solve the problem.
Therefore I attempt to solve it and expose programmatic interface via PyPI.
I also put my [answer](https://stackoverflow.com/a/57574429/7881370) to the question above.

This repo is adapted from [my Gist](https://gist.github.com/kkew3/d1eed0984a3a44087c700215e99eefd2).


Install
-------

```bash
pip install sliceparser
# or pip3 install sliceparser
```


Usage
-----

```python
import sliceparser
a = [1,2,3,4]
assert a[sliceparser.parse_slice('2:')] == a[2:]
assert a[sliceparser.parse_slice('::2')] == a[::2]
assert a[sliceparser.parse_slice('1')] == a[1]

import numpy as np
A = np.eye(3)
assert np.array_equal(A[sliceparser.parse_slice('0, 1:')], A[0,1:])
assert np.array_equal(A[sliceparser.parse_slice('..., 2')], A[..., 2])
```

etc.
