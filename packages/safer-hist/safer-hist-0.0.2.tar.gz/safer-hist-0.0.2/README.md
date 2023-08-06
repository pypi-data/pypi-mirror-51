# SAFER STORAGE NAS Historical management

This project implements a system level API to query and manage the SAFER-STORAGE backup and storage in space and time dimensions (hence the historical dimension). Each command of this API is designed to be either invoked directly from the shell or wrapped into an higher level API, eg. a web-ui back-end.

The SAFER-STORAGE backup system is extensively based on [ZoL](https://zfsonlinux.org/) snapshots as found in particulat in the [Proxmox VE](https://pve.proxmox.com/wiki/Main_Page) distribution. Notice that some features may be unavailable depending on which ZoL version is available on the execution platform.

## Install

This project uses [python v3.7.4](https://docs.python.org/3.7/). We recommend installing python using [pyenv](https://github.com/pyenv/pyenv#installation) eg. with the [pyenv installer](https://github.com/pyenv/pyenv-installer), as a regular (non-root) user:

```bash
$ curl https://pyenv.run | bash
$ pyenv install 3.7.4
$ pyenv local 3.7.4
```
Note that if python is already installed or you are already pyenv but an older version, version 3.7.4 may not be available. Simply erase your previous pyenv installation an reinstall from scratch (or use vagrant, for a clean fresh start).

This package is then available through PyPI using the following command:
```bash
$ pip install --upgrade safer_hist_pkg
```

## Usage

### `safer` : main command

The commands of this package are part of a module named safer_hist. For convenience, we also recommend defining the following funtion in your shell (eg. in your `.bashrc`):
```bash
function safer() 
{
    case $1 in
        help|lssnaps|genmeta|lsuntil|lsalltime|restore)
            subcmd=$1
            shift
            python -m safer_hist ${subcmd} "$@"
            ;;
        *)
            python -m safer_hist help "$@"
            ;;
    esac
}
```

### `safer genmeta`: Snapshot meta-info generation 

Generates a snapshot meta file for the snapshot `@<snapshot>` of the (ZFS) dataset `<dataset>`. By default the output is written to a file named `.zfsmeta_<snapshot>` at the root of the dataset. If `-o` option is given, output is written to the specied filename or to stdout if `-` (minus) is given instead of a filename.

```bash
$ safer genmeta [-o file|-] dataset@snapshot
```

### `safer lssnaps`: Snapshot list

### `safer lsuntil`: Merge target dir content from snapshots until

### `safer lsalltime`: Marge target dir content from all snapshots

### `safer restore`: Restore file from snapshot

## Packaging and deploying to PyPI
(reminder, see this [tuto](https://packaging.python.org/tutorials/packaging-projects/))

Install building dependencies as follows:
```bash
$ python3 -m pip install --upgrade setuptools wheel
```

Build package as follows:
```bash
$ python3 setup.py sdist bdist_wheel
```

Upload to PyPI server:
```bash
$ python3 -m twine upload dist/*
```

## License
[Licensed under the EUPL](https://choosealicense.com/licenses/eupl-1.2/)

## Author(s)

* DALLE, Olivier (First.LAST@safer-storage.com)



