# pipdeps

Pipdeps shows/upgrades outdated packages with respect to existing dependencies.

Python 2.7 is required.

## Usage

```console
$ pipdeps.py --help
usage: pipdeps.py [-h] (-l | -u | -s SHOW [SHOW ...])

Pipdeps shows/upgrades outdated packages with respect to existing
dependencies.

optional arguments:
  -h, --help            show this help message and exit
  -l, --list            show upgradeable packages and versions
  -u, --upgrade         upgrade upgradeable packages
  -s SHOW [SHOW ...], --show SHOW [SHOW ...]
                        show detailed info about upgradeable packages
```

## Changelog


## 0.0.3 (2019-08-29)

### Other

* Case vanished module; all deps are taken from metadata; hotfix extras. [Marek Chrastina]


## 0.0.2 (2019-08-16)

### Other

* Remove version.py. [Marek Chrastina]

* Add history. [Marek Chrastina]


## 0.0.1 (2019-08-16)

### Other

* Add documentation to CI. [Marek Chrastina]

* Add install test, version check and deploy to CI. [Marek Chrastina]

* Add pycodestyle to CI. [Marek Chrastina]

* Add show option. [Marek Chrastina]

* Requires of possible upgradable package versions has to be taken into account. [Marek Chrastina]

* Collect data for all packages. [Marek Chrastina]

* Upgrade pip first. [Marek Chrastina]

* Check for python version. [Marek Chrastina]

* Tabulate print list. [Marek Chrastina]

* Add list option. [Marek Chrastina]

* Code refactoring. [Marek Chrastina]

* Make pylint happy. [Marek Chrastina]

* Add build ci. [Marek Chrastina]

* Add setup.py and __init__.py. [Marek Chrastina]

* Add py script. [Marek Chrastina]

* Add LICENSE. [Marek Chrastina]

* Add README. [Marek Chrastina]


