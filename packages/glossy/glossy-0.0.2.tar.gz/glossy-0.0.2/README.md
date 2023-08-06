
![](docs/img/slogan.gif)


<br/>

## Installation

```
pip install glossy
```

<br/>

## Start Decorating

```python
import glossy
import time


@glossy.decorator
def timer(func, *args, **kwargs):
    """
    Timer

    Place this decorator on functions to see how long
    they take to execute.
    """
    start = time.time()
    result = func(*args, **kwargs)
    secs = time.time() - start
    name = func.__name__
    print(f"Function {name} took {secs} seconds")
    return result
```
<br/>


# Features

* [Flatter Decorators](docs/pages/flatten.md)
* [Discoverabilty](#discovery)
* [Testing & Mocking](#testing)
