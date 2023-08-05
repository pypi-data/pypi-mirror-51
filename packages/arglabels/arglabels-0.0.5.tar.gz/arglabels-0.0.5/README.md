# arglabels

[![Build Status](https://travis-ci.com/michael-harms/arglabels.svg?branch=master)](https://travis-ci.com/michael-harms/arglabels) [![License: MIT](https://img.shields.io/pypi/l/arglabels)](https://github.com/michael-harms/arglabels/blob/master/LICENSE)

A simple decorator to enable Swift-like argument labels for functions.

It re-labels certain keyword arguments, so that your function parameters can have an external and an internal name like [argument labels and parameter names](https://docs.swift.org/swift-book/LanguageGuide/Functions.html#ID166) in Swift.

## Installation

Install from PyPI with:

```
pip install arglabels
```

## Usage

If you have a function like the following:

```python
def invite(name, activity):
    return f"Hey {name}! Would you like to go {activity}?"
```

When calling that function it would be nice to have a syntax that almost reads like plain english, for example:

```python
invite("Alex", to_go="fishing")
```

You can achieve this with the arglabels decorator, by using it on the function definition like so:

```python
from arglabels import arglabels

@arglabels(activity="to_go")
def invite(name, activity):
    return f"Hey {name}! Would you like to go {activity}?"
```
