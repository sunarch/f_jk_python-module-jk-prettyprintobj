﻿jk_prettyprintobj
========

Introduction
------------

This python module provides a mixin for dumping objects. This is ment for debugging purposes: Sometimes it is very convenient to have a way of writing all data of an object to STDOUT in a human readable way. This module assists in such implementations.

Information about this module can be found here:

* [github.org](https://github.com/jkpubsrc/python-module-jk-prettyprintobj)
* [pypi.python.org](https://pypi.python.org/pypi/jk_prettyprintobj)

How to use this module
----------------------

### Import the module

In order to use this module you need to import it first. So add this line to the head of your python source code file:

```python
import jk_prettyprintobj
```

### Use the provided mixin

To make use of the features of this module you must add a mixin to your class. Example:

```python
class ExampleClass(jk_prettyprintobj.DumpMixin):

	def __init__(self, ...):
		...

	...
```

If you derive your class from a base class just add the mixin to your list of base classes. The order does not matter in this case. Here is an example how to do this:

```python
class MyFancyException(Exception, jk_prettyprintobj.DumpMixin):

	def __init__(self, msg:str):
		super().__init__(msg)

	...
```

In this example we use `Exception` as a base class to keep this example simple. It just demonstrates the technique. You can use any base class for inheritance, it is just necessary that you somewhere in the list of base classes add `jk_prettyprintobj.DumpMixin`. This does not yet make use of the features provided by `jk_prettyprintobj` but prepares its use.

This mixin adds a regular method named `dump()` to the class. For all things to work it is important that you have no other method named `dump()` in your class that might conflict with the implementation provided by `DumpMixin`. This method can be called later, but some additional implementation steps need to be taken first. (See next section!)

### Implement a helper method

To actually enable the class to produce output we must implement one of the helper methods. These are:

| **Method name**									| **Description**								|
| ---												| ---											|
| `_dump(ctx:jk_prettyprintobj.DumpCtx) -> None`	| Implement dumping data on your own			|
| `_dumpVarNames() -> typing.List[str]`				| Provide the names of the variable to output	|

More to these options in the next sections.

### Helper method _dumpVarNames()

If you implement the method `_dumpVarNames() -> typing.List[str]` your method needs to return a list of variable names that should be dumped to STDOUT.

Here is an example of a simple but working implementation.

```python
class Matrix(jk_prettyprintobj.DumpMixin):

	def __init__(self, m):
		self.m = m
		self.nRows = len(m)
		self.nColumns = len(m[0])

	def _dumpVarNames(self) -> list:
		return [
			"nRows",
			"nColumns",
			"m",
		]
```

Now what `_dumpVarNames()` will do is simply returning a list of variables to access for output.

As private variables can not be accessed by mixins all variables in this example have therefore been defined as public variables. This is a general limitation of python so there is no way around this: All variables to output this way need to be non-private.

Now let's create an instance of `Matrix` and invoke `dump()`:

```python
m = Matrix([
	[	1,	2,	3 	],
	[	4,	5,	6 	],
	[	7,	8,	9.1234567	],
])

m.dump()
```

If `dump()` is invoked on an initialized instance of `Matrix` from this example such an object will render to something like this:

```
<Matrix(
	nRows = 3
	nColumns = 3
	m = [
		[ 1, 2, 3 ],
		[ 4, 5, 6 ],
		[ 7, 8, 9.1234567 ],
	]
)>
```

### Helper method _dump(ctx)

If you implement the method `_dump(ctx:jk_prettyprintobj.DumpCtx) -> None` your method needs to use the provided context object to implement dumping variables to STDOUT on your own. This variant is helpful if you - for some reason - require to output private variables that an implementation of `_dumpVarNames()` will not be able to access.

By implementing this method you will also be able to modify the way how the contents of a variable will be written to STDOUT.

Here is an example of a simple but working implementation:

```python
class Matrix(jk_prettyprintobj.DumpMixin):

	def __init__(self, m):
		self.__m = m
		self.__nRows = len(m)
		self.__nColumns = len(m[0])

	def _dump(self, ctx:jk_prettyprintobj.DumpCtx):
		ctx.dumpVar("nRows", self.__nRows)
		ctx.dumpVar("nColumns", self.__nColumns)
		ctx.dumpVar("m", self.__m, "float_round3")
```

This class is expected to represent a mathematical matrix and therefore should receive a two-dimensional field of `float` values during construction. During construction this data is stored in a private variable named `__m`. Additional private variables are created. For simplicity no other methods except `dump_()` are implemented in this example.

Now what `_dump()` will do is to invoke `dumpVar()` for every single variable. `dumpVar()` has the following signature:

* `dumpVar(varName:str, value, postProcessorName:str = None) -> None`

This method requires to receive up to three arguments:
* `str varName`: The name to use for output. In this example we use `nRows` as we might add a property of exactly this name. (Not implemented in this example!)
* `* value`: A value of any kind. This is the value that should later on be written to STDOUT.
* `str processorName`: This optional value can be one of several identifiers that indicate how to process the value *before* it is converted to a string. (See section below.)

If `dump()` is invoked on an initialized instance of `Matrix` from this example such an object will render to something like this:

```
<Matrix(
	nRows = 3
	nColumns = 3
	m = [
		[ 1, 2, 3 ],
		[ 4, 5, 6 ],
		[ 7, 8, 9.123 ],
	]
)>
```

Please note that in this case the output of the very last `float` in the matrix might be rounded to three digits as defined by the processor `float_round3`. This is different to an implementation providing `_dumpVarNames()`.

### Processors

For producing output you can apply a processor that will preprocess the output before writing it to STDOUT. This is useful to achieve a more human readable representation of data in some cases.

These are the processors you can use:

| **Name**			| **Description**				|
| ---				| ---							|
| `float_round1`	| Round to 1 fractional digit	|
| `float_round2`	| Round to 2 fractional digit	|
| `float_round3`	| Round to 3 fractional digit	|
| `float_round4`	| Round to 4 fractional digit	|
| `float_round5`	| Round to 5 fractional digit	|
| `float_round6`	| Round to 6 fractional digit	|
| `float_round7`	| Round to 7 fractional digit	|
| `int_hex`			| Convert to hexadecimal representation		|
| `int_bit`			| Convert to binary representation		|
| `str_shorten`		| Shorten a string to at most 40 characters. If you have objects with large amounts of text this feature can make your output more readable.	|

Futher Development
-------------------

It is likely that future developments will add more alternatives for dumping an objects. If you have any ideas, requirements or recommendations please feel free to leave a comment.

Contact Information
-------------------

This is Open Source code. That not only gives you the possibility of freely using this code it also
allows you to contribute. Feel free to contact the author(s) of this software listed below, either
for comments, collaboration requests, suggestions for improvement or reporting bugs:

* Jürgen Knauth: pubsrc@binary-overflow.de

License
-------

This software is provided under the following license:

* Apache Software License 2.0



