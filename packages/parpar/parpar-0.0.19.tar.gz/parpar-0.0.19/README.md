# About
ParPar (Parallel Parser) is a light tool which makes it easy to distribute a function across a large file.

ParPar is meant to work on serialized data where some values are highly repeated across records for a given field. e.g.

```
a 1 1
a 1 2
a 2 3
a 2 4
a 3 5
a 3 6
b 1 7
b 1 8
b 2 9
b 2 10
b 3 11
b 3 12
```

although we have 12 records, for column 1 there are only 2 unique values. Likewise, for column 2 there are only 3 unique values. We could break this file up into smaller files under a directory:

```
<out-dir>/<col-1-value>/<col-2-value>
```
or vis versa.

# How to use.

1. Start by importing the ParPar class:

```python
from parpar import ParPar
```

2. Initialize an instance:

```python
ppf = ParPar()
```

3. Shard a large file into sub-files:

```python
# shard by columns
ppf.shard(
  <input-file>, <output-directory>,
  <columns>, <delim>, <newline>
)

# shard by lines
ppf.shard_by_lines(
  <input-file>, <output-directory>,
  <number_of_lines>, <delim>, <newline>
)
```

4. Check to make sure the number of records are the same:

```python
files = ppf.shard_files(<output-directory>)
records = ppf.sharded_records(files)

from parpar.utils import filelines

print(records == filelines(<input-file>))
```


5. Map an arbitrary function across each _line_ of all shared files:

```python
def foo(line, *args, **kwargs):
    pass

args = [1, 2, 3]
kwargs = {'a': 'x', 'b': 'y'}

ppf.shard_line_apply(<output-directory>,
  foo, args, kwargs,
  processes=<number-of-processes>
)
```


6. Map an arbitrary function across all shared files:

```python
def bar(file, *args, **kwargs):
    pass

args = [1, 2, 3]
kwargs = {'a': 'x', 'b': 'y'}

ppf.shard_file_apply(<output-directory>,
  bar, args, kwargs,
  processes=<number-of-processes>
)
```
