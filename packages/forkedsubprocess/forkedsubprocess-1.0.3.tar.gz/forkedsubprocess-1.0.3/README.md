[![pipeline status](https://gitlab.devlabs.linuxassist.net/allworldit/python/forkedsubprocess/badges/master/pipeline.svg)](https://gitlab.devlabs.linuxassist.net/allworldit/python/forkedsubprocess/commits/master)
[![coverage report](https://gitlab.devlabs.linuxassist.net/allworldit/python/forkedsubprocess/badges/master/coverage.svg)](https://gitlab.devlabs.linuxassist.net/allworldit/python/forkedsubprocess/commits/master)

# Forked subprocess support for Python

This package allows for the running of a subprocess in the background, including the sending of data to the subprocess and
receiving of data from it. Threads are used to achieve the reading/writing of data.


## Basic usage

```python
from forkedsubprocess import ForkedSubprocess

process = ForkedSubprocess(['cat'])
process.run()
process.send('some string')
returncode = process.wait()

stdout = process.stdout
stderr = process.stderr
output = process.output
```


## Writing output to console

Output can be written to the console at the same time using `enable_output=True`.

```python
from forkedsubprocess import ForkedSubprocess

process = ForkedSubprocess(['cat'], enable_output=True)
process.run()
process.send('some string')
returncode = process.wait()

stdout = process.stdout
stderr = process.stderr
output = process.output
```


## Using a callback

A callback can be used for each line of output received.

```python
from forkedsubprocess import ForkedSubprocess

def my_callback(line: str):
	print(f'LINE: {line}')

process = ForkedSubprocess(['cat'], output_callback=my_callback)
process.run()
process.send('some string')
returncode = process.wait()

stdout = process.stdout
stderr = process.stderr
output = process.output
```


# License
<pre>
Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
</pre>
