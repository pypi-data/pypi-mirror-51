# performer

Lightweight benchmarking decorator.

## Installation
```
$ pip3 install performer
```

## Usage

All benchmark results are output after the program ends.  
The benchmark decorator does not affect the function output.

```python
from performer import benchmark

@benchmark(1000)
def sum_range(n):
    return sum(range(n))

@benchmark(100)
def hello():
    return "Hello"

print(sum_range(100))
print(hello())
```