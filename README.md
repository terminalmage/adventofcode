# Advent of Code

My scripts for [Advent of Code](https://adventofcode.com).

These scripts are written in Python 3, and some of them use syntax introduced
in Python 3.8 (the "[walrus operator](https://peps.python.org/pep-0572)"), 3.10
([Structural Pattern Matching](https://peps.python.org/pep-0636)), and 3.11
([self-typing](https://peps.python.org/pep-0673)). If you do not have Python
3.11 available and would like to run these scripts, you have a couple options:

1. Use the [official Docker images](https://hub.docker.com/_/python/) for
   Python. For example, from the root of this git repository, run the
   following command:

   ```bash
   docker run --rm -it -v $PWD:/scripts python:3.11-slim bash
   ```

   This will give you a bash shell, from which you can `cd` to the bind-mounted
   scripts dir and run the scripts:

   ```bash
   cd /scripts/2022
   ./day01.py
   ```

   When done, exit from the shell (run `exit` or use Ctrl-d) and the container
   will be destroyed.

2. Use
   [pyenv](https://github.com/pyenv/pyenv#simple-python-version-management-pyenv)
   to build a Python 3.11 (or newer) release. This will also require that you
   have installed the [build
   dependencies](https://github.com/pyenv/pyenv/wiki#suggested-build-environment).

## INPUTS

You must provide your own inputs. Per the
[FAQ](https://old.reddit.com/r/adventofcode/wiki/faqs/copyright/inputs), inputs
should not be publicly shared. In my repo, I solve this by storing my inputs in
a [git submodule](https://git-scm.com/book/en/v2/Git-Tools-Submodules) which is
a separate, private repo. To run these scripts with your own inputs, you must
copy them into your clone of this repo at the following path:
`inputs/YYYY/dayDD.txt`, where `YYYY` is the 4-digit year, and `DD` is the
two-digit date. So, for example, 2022 day 7 would be `inputs/2022/day07.txt`.
