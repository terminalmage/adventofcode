# Advent of Code

My scripts for [Advent of Code](https://adventofcode.com).

These scripts are written in Python 3, and some of them use syntax introduced
in Python 3.8 (the "[walrus operator](https://peps.python.org/pep-0572)") and
3.10 ([Structural Pattern Matching](https://peps.python.org/pep-0636)). If you
do not have Python 3.10 available and would like to run these scripts, you have
a couple options:

1. Use the [official Docker images](https://hub.docker.com/_/python/) for
   Python. For example, from the root of this git repository, run the
   following command:

   ```bash
   docker run --rm -it -v $PWD:/scripts python:3.10-slim bash
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
   to build a Python 3.10 release. This will also require that you have
   installed the [build
   dependencies](https://github.com/pyenv/pyenv/wiki#suggested-build-environment).
