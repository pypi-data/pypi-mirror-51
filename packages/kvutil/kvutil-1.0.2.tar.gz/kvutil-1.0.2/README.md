# kvutil: a command-line key-value store
A command-line program written in Python 3.7 to wrap a dbm implementation in order to store key-value pairs.  kvutil has no third-party requirements outside of the Python 3.7 standard library.

## Usage
#### Insert a key+value
```
kv mykey myvalue
```

#### Read a value
```
kv mykey
```

#### List all keys
```
kv -l
```

#### Delete a key+value
```
kv -rm mykey
```

## Installation
kvutil requires Python 3.6+.

### From PyPI
```
pip install kvutil
```

### From source, using [Pyinstaller](https://pyinstaller.readthedocs.io/en/stable/index.html)
First, install a Python 3.6+ environment.

Then, run the following commands:
```
$ #clone repository
$ git clone https://github.com/mhv2109/kvutil.git && cd kvutil
$ #use the latest pip
$ pip install --upgrade pip
$ #install pyinstaller using pip
$ pip install pyinstaller
$ # create a single-file executable using pyinstaller
$ pyinstaller --onefile kvutil/kv.py
```

The resulting executable can be found in `dist/`.

## Development
kvutil requires Python 3.6+.

Development dependencies are found in `requirements.txt`. Install them with `pip install -r requirements.txt`.

Tests are run using the built-in [unittest](https://docs.python.org/3.7/library/unittest.html) framework and [tox](https://tox.readthedocs.io/en/latest/index.html).