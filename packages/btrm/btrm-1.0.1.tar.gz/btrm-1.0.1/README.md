# Btrm
![build status](https://img.shields.io/badge/build-passing-green)
![python version](https://img.shields.io/badge/python-2.7.16-blue)
![license](https://img.shields.io/badge/license-MIT-red)
> Alternative tool for rm command in linux using python
---
## Table of content
* [Introduction](#introduction)
* [Requirement](#requirement)
* [Installation](#installation)
* [Configuration](#configuration)
* [Usage](#usage)
* [Example](#example)
* [Contribute](#contributing)
* [License](#license)
---
## Introduction
- Btrm stand for "backup then remove", this project aim to replace build-in command rm in Unix system.
- The rm -rf command is one of the fastest way to delete a folder and its contents. But a little typo or ignorance may result into unrecoverable system damage. So we decide to built our alternative tool to remove file but with **backup mechanism**. 
---
## Requirement
- python 2.7
---
## Installation
```
pip install --user btrm
```
---
## Configuration
- Edit default config at ~/.config/btrm.conf
---
## Usage
```
usage: btrm.py [OPTION]... [FILE]...

Alternative tool for rm command in linux using python

positional arguments:
  filename             directory or file you want to delete

optional arguments:
  -h, --help           show this help message and exit
  -i                   prompt before removal (default)
  -f, --force          force delete without promt
  -r, -R, --recursive  remove directories and their contents recursively
  --no-backup          remove without backup mechanism (can not recover later)
  --recover            recover file from trash
  --list-trash         show list deleted file, sort by date time
  --wipe-all           complete delete everything from recycle bin, free disk
                       space
  -v, --version        show version information and exit

By default, btrm does not remove directories.  Use the --recursive (-r or -R)
option to remove each listed directory, too, along with all of its contents.

To remove a file whose name starts with a '-', for example '-foo',
use one of these commands:
  btrm -- -foo

  btrm ./-foo

Note that if you use btrm to remove a file, it always be possible to recover all 
of its contents within 60 days, looking for deleted file at trash directory and
and use --recover options to recover whatever you want. For greater assurance 
that the contents are truly unrecoverable, consider using shred.
```
---
## Example
- Remove directory xyz and abc
![](sources/resources/images/remove_example.png)

- show list removed file
![](sources/resources/images/show_list.png)

- recover directory xyz and abc
![](sources/resources/images/recover_example.png)
