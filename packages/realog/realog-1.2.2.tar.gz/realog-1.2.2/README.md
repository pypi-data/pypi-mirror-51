Atria Debug
===========

`atria debug` is a simple python librairy that permit to display application logs on console with a atria level.


[![Badge](https://badge.fury.io/py/realog.png](https://pypi.python.org/pypi/realog)


Instructions
------------

Simply include the log system:
```
  from realog import debug
```

Configure the level:
```
## Set log level of the console log system
## parameter: Value of the log level:
##              0: None
##              1: error
##              2: warning
##              3: info
##              4: debug
##              5: verbose
##              6: extreme_verbose
debug.set_level(6)
```

Enable the color:
```
enable_color()
disable_color()
```

Use it:
```
debug.error("lkjlkjlkj" + "kljhlkj" + str(1513))
debug.warning("lkjlkjlkj" + "kljhlkj" + str(1513))
debug.ingo("lkjlkjlkj" + "kljhlkj" + str(1513))
debug.debug("lkjlkjlkj" + "kljhlkj" + str(1513))
debug.verbose("lkjlkjlkj" + "kljhlkj" + str(1513))
debug.extreme_verbose("lkjlkjlkj" + "kljhlkj" + str(1513))
```

git repository
--------------

http://github.com/HeeroYui/realog/

Documentation
-------------

http://HeeroYui.github.io/realog/

Installation
------------

Requirements: ``Python >= 2.7`` and ``pip``

Just run:
```
pip install realog
```

Install pip on debian/ubuntu:
```
sudo apt-get install pip
```

Install pip on ARCH-linux:
```
sudo pacman -S pip
```

Install pip on MacOs:
```
sudo easy_install pip
```

License (MPL v2.0)
---------------------

Copyright realog Edouard DUPIN

Licensed under the Mozilla Public License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.mozilla.org/MPL/2.0/

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

