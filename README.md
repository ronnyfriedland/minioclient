# minioclient
Minio / S3 graphical client written in python

## Configuration

The configuration is stored in `config.ini` which is generated after initial startup.

## Configuration example

```
[minio]
url = <host>:<port>
accesskey = .....
secretkey = .....
ssl = <True|False>
debug = <True|False>

[logging]
loglevel = <DEBUG|INFO|WARN|ERROR>
```

# Modules

To define Python modules which enables you to import classes in this module is very simple. 
You just have to add an empty `__init__.py` file in the directory.

[Example](client/__init__.py)

# Documentation

To document implementation details you should use the python standard [Docstrings](https://www.python.org/dev/peps/pep-0257/)

If you want to create a HTML documentation based on the Docstring you can use pdoc 
which simply generates a nice formatted HTML page.

# Logging

For this project I use the [standard logging module](https://docs.python.org/3/library/logging.html).
A special [Configuration](config/LoggingConfiguration.py) - class handles the initialization and configuration to encapsulates logging setup.

# Unit-Tests

Simple python classes are tested with the [standard unittest module](https://docs.python.org/3/library/unittest.html).

PyQT dialogs are testable the same way - see [tests/test-loginwidget.py]

To verify the coverage of the test, you can verify it using `coverage` module:

- execute coverage run: `coverage run -a -m unittest tests/test-*`
- create report: `coverage report -m`

```
Name                                                                                     Stmts   Miss  Cover   Missing
----------------------------------------------------------------------------------------------------------------------
client/MinioClient.py                                                                       28      7    75%   50-53, 62, 71, 79
client/__init__.py                                                                           0      0   100%
config/Configuration.py                                                                     18      1    94%   32
config/MinioConfiguration.py                                                                19      6    68%   30-35
config/__init__.py                                                                           0      0   100%
widgets/LoginPage.py                                                                        29      1    97%   53
widgets/__init__.py                                                                          0      0   100%
```

# Threading

TODO: describe
