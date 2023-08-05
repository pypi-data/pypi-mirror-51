# Cache Function

You can use this python decorator
[Github-flavored Markdown](https://github.com/deepakmishra/cache_function/)
to cache a result of a function.

## Installation
pip install -i https://test.pypi.org/simple/ cache-function-deepakmishra

## Usage

### Production Setting
```python
from cache_function import cache_function
cache_function.cache = **your cache object which has get and set functions**
```

### Development Setting
```python
from cache_function import cache_function, test_cache_function
cache_function.cache = test_cache_function.DummyCache()
```

### Usage: Cache a function result
```python
from cache_function.cache_function import cache_function

@cache_function(expiry=30) # time in seconds
def foo(a, b, c):
    return a + b + c
```
