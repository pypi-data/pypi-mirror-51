qworktree
=====

`qworktree` is a simple tool to permit to manage a qt worktree without managing the main xxx.pro.

It is designed to create the main pro file at the root path of the tree (where you execute it it.

It have some containts that I does not arrive to remove:

*  need to declate the MK_FEATURE element
*  generate 2 file in the root directory


Instructions
------------

This tool is to create the main .pro file of your worktree

qworktree is under a FREE license that can be found in the LICENSE file.
Any contribution is more than welcome ;)

git repository
--------------

http://github.com/HeeroYui/qworktree/

Installation
------------

Requirements: ``Python >= 2.7`` and ``pip``

Just run:
```
pip install qworktree
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

Usage
-----

Download your worktree and run the command

```
qworktree
export QMAKEFEATURES=`pwd`/mkfeatures
mkdir build
cd build
qmake ..
```

the qworktree will generate local files

```
folder_name.pro ==> the file of the worktree description
defines.prf ==> a file that define a list of dependency macro
```

Creating the needed elements
----------------------------

1: Need a mkfeature to add an include to determine the main root worktree: ```mkfeatures/root_directory.prf```

```
ROOT_DIRETORY += $${PWD}/..
ROOT_DEFINES += $${PWD}/../defines.prf
load(../defines.prf)
```

2: Create a file in your library/plugin/application folder: ```folderName/qworktree_folderName.py```

```
#!/usr/bin/python
# -*- coding: utf-8 -*-
depend_on = [
"depend_worktree_lib1_name",
"depend_worktree_lib2_name"
	]
```

3: Create a file in your worktree with the dependency property: ```folderName/dependencies.pri```

```
INCLUDEPATH += $$PWD
LIBS *= -llibraryName
```

4: Import the library elements:

```
  load(root_directory.prf)
  # request include properties
  include($$ROOT_DIRETORY/$$LIB_DECLARE_DEPENDENCIES_FOLDERNAME1)
  include($$ROOT_DIRETORY/$$LIB_DECLARE_DEPENDENCIES_MYLIB2)
```

Note that the define is generate in the file ```defines.prf```


License (MPL v2.0)
------------------

Copyright qworktree Edouard DUPIN

Licensed under the Mozilla Public License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at


    https://www.mozilla.org/MPL/2.0/

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

