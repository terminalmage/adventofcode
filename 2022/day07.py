#!/usr/bin/env python
'''
https://adventofcode.com/2022/day/7

--- Day 7: No Space Left On Device ---

You can hear birds chirping and raindrops hitting leaves as the expedition
proceeds. Occasionally, you can even hear much louder sounds in the distance;
how big do the animals get out here, anyway?

The device the Elves gave you has problems with more than just its
communication system. You try to run a system update:

$ system-update --please --pretty-please-with-sugar-on-top Error: No space left
on device

Perhaps you can delete some files to make space for the update?

You browse around the filesystem to assess the situation and save the resulting
terminal output (your puzzle input). For example:

$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k

The filesystem consists of a tree of files (plain data) and directories (which
can contain other directories or files). The outermost directory is called /.
You can navigate around the filesystem, moving into or out of directories and
listing the contents of the directory you're currently in.

Within the terminal output, lines that begin with $ are commands you executed,
very much like some modern computers:

- cd means change directory. This changes which directory is the current
  directory, but the specific result depends on the argument:

    - cd x moves in one level: it looks in the current directory for the
      directory named x and makes it the current directory.

    - cd .. moves out one level: it finds the directory that contains the
      current directory, then makes that directory the current directory.

    - cd / switches the current directory to the outermost directory, /.

- ls means list. It prints out all of the files and directories immediately
  contained by the current directory:

    - 123 abc means that the current directory contains a file named abc with
      size 123.

    - dir xyz means that the current directory contains a directory named xyz.

Given the commands and output in the example above, you can determine that the
filesystem looks visually like this:

- / (dir)
  - a (dir)
    - e (dir)
      - i (file, size=584)
    - f (file, size=29116)
    - g (file, size=2557)
    - h.lst (file, size=62596)
  - b.txt (file, size=14848514)
  - c.dat (file, size=8504156)
  - d (dir)
    - j (file, size=4060174)
    - d.log (file, size=8033020)
    - d.ext (file, size=5626152)
    - k (file, size=7214296)

Here, there are four directories: / (the outermost directory), a and d (which
are in /), and e (which is in a). These directories also contain files of
various sizes.

Since the disk is full, your first step should probably be to find directories
that are good candidates for deletion. To do this, you need to determine the
total size of each directory. The total size of a directory is the sum of the
sizes of the files it contains, directly or indirectly. (Directories themselves
do not count as having any intrinsic size.)

The total sizes of the directories above can be found as follows:

- The total size of directory e is 584 because it contains a single file i of
  size 584 and no other directories.

- The directory a has total size 94853 because it contains files f (size
  29116), g (size 2557), and h.lst (size 62596), plus file i indirectly (a
  contains e which contains i).

- Directory d has total size 24933642.

- As the outermost directory, / contains every file. Its total size is
  48381165, the sum of the size of every file.

To begin, find all of the directories with a total size of at most 100000, then
calculate the sum of their total sizes. In the example above, these directories
are a and e; the sum of their total sizes is 95437 (94853 + 584). (As in this
example, this process can count files more than once!)

Find all of the directories with a total size of at most 100000. What is the
sum of the total sizes of those directories?

--- Part Two ---

Now, you're ready to choose a directory to delete.

The total disk space available to the filesystem is 70000000. To run the
update, you need unused space of at least 30000000. You need to find a
directory you can delete that will free up enough space to run the update.

In the example above, the total size of the outermost directory (and thus the
total amount of used space) is 48381165; this means that the size of the unused
space must currently be 21618835, which isn't quite the 30000000 required by
the update. Therefore, the update still requires a directory with total size of
at least 8381165 to be deleted before it can run.

To achieve this, you have the following options:

- Delete directory e, which would increase unused space by 584.
- Delete directory a, which would increase unused space by 94853.
- Delete directory d, which would increase unused space by 24933642.
- Delete directory /, which would increase unused space by 48381165.

Directories e and a are both too small; deleting them would not free up enough
space. However, directories d and / are both big enough! Between these, choose
the smallest: d, increasing unused space by 24933642.

Find the smallest directory that, if deleted, would free up enough space on the
filesystem to run the update. What is the total size of that directory?
'''
from __future__ import annotations
import errno
import os
import re
import sys
from collections.abc import Iterator

# Local imports
from aoc2022 import AOC2022


class PathBase:
    '''
    Base class for Directory and File objects
    '''
    def __init__(self, name: str, parent: Directory|None) -> None:
        '''
        Create an empty directory
        '''
        self.name = name
        self.parent = parent

    @property
    def parent(self):
        '''
        Return the parent directory
        '''
        return self.__parent

    @parent.setter
    def parent(self, value: Directory|None) -> None:
        '''
        Validate and set the parent
        '''
        if not (value is None or isinstance(value, Directory)):
            raise ValueError(
                f'Expected Directory or NoneType, not {type(value).__name__}'
            )
        self.__parent = value

    @parent.deleter
    def parent(self) -> None:
        '''
        Don't allow attribute to be deleted
        '''

    @property
    def path(self):
        '''
        Return the absolute path of this file/directory
        '''
        components = [self.name]
        ptr = self
        # Walk back up until you reach the root, adding to the list
        while (ptr := ptr.parent).name != os.path.sep:
            components.append(ptr.name)

        return os.path.sep + os.path.sep.join(reversed(components))


class File(PathBase):
    '''
    Represents a single file
    '''
    def __init__(
        self,
        name: str,
        parent: Directory|None,
        size: int,
    ) -> None:
        '''
        Initialize the object
        '''
        super().__init__(name, parent)
        self.size = size

    def __repr__(self) -> str:
        '''
        Define repr() output
        '''
        return f'File(name={self.name!r}, parent={self.parent!r}, size={self.size!r})'


class Directory(PathBase):
    '''
    Represents a directory in a filesystem
    '''
    def __init__(
        self,
        name: str = '/',
        parent: Directory|None = None,
    ) -> None:
        '''
        Create an empty directory
        '''
        if parent is None:
            name = '/'
        elif name == '/':
            raise ValueError(f'Directory name cannot contain {name!r}')

        super().__init__(name, parent)
        self.contents = {}

    def __repr__(self) -> str:
        '''
        Define repr() output
        '''
        return f'Directory(name={self.name!r}, parent={self.parent!r})'

    def __iter__(self) -> Iterator[Directory|File]:
        '''
        Define repr() output
        '''
        return iter(self.contents.values())

    def __getitem__(
        self,
        path: str,
    ) -> Directory|File:
        '''
        Return the Directory or File object at the relative path
        '''
        if os.path.isabs(path):
            raise ValueError('Only relative paths can be referenced')

        ptr = self

        for split in path.split(os.path.sep):
            match split:
                case '.' | '':
                    pass
                case '..':
                    ptr = ptr.parent
                case _:
                    if split not in ptr.contents:
                        raise FileNotFoundError(
                            errno.ENOENT,
                            os.strerror(errno.ENOENT),
                            path,
                        )
                    ptr = ptr.contents[split]

        return ptr

    def __setitem__(
        self,
        name: str,
        val: Directory|File,
    ) -> None:
        '''
        Assign a file/directory
        '''
        self.contents[name] = val

    def mkdir(
        self,
        name: str,
    ) -> None:
        '''
        Create a new subdir within this directory
        '''
        if os.path.sep in name:
            raise ValueError('Cannot create multiple directory levels')

        self[name] = Directory(name, parent=self)

    def add(
        self,
        name: str,
        size: int,
    ) -> None:
        '''
        Add a file in this directory
        '''
        self[name] = File(name, parent=self, size=size)

    @property
    def size(self) -> int:
        '''
        Return the size of the contents of this directory
        '''
        return sum(item.size for item in self.contents.values())

    def dirs(self, recurse: bool = False) -> Iterator[Directory]:
        '''
        Generator function to return the directories within this directory
        '''
        for item in self:
            if isinstance(item, Directory):
                yield item
                if recurse:
                    for subdir in item.dirs(recurse=recurse):
                        yield subdir

    def files(self, recurse: bool = False) -> Iterator[File]:
        '''
        Generator function to return the files within this directory
        '''
        for item in self:
            if isinstance(item, File):
                yield item
            else:
                if recurse:
                    for fileobj in item.files(recurse=recurse):
                        yield fileobj


class AOC2022Day7(AOC2022):
    '''
    Day 7 of Advent of Code 2022
    '''
    day = 7
    disk_size = 70_000_000

    def __init__(self, example: bool = False) -> None:
        '''
        Load the datastream
        '''
        super().__init__(example=example)
        self.rootdir = Directory('/')

        line_re = re.compile(r'^(\$|\d+|dir) (.+)')
        ls = False

        cwd = self.rootdir

        with self.input.open() as fh:
            try:
                while (line := next(fh).rstrip(os.linesep)):
                    id_, rest = line_re.match(line).groups()
                    if id_ == '$':
                        if rest.startswith('cd '):
                            dest = rest[3:]
                            ls = False
                            if dest == os.path.sep:
                                cwd = self.rootdir
                            else:
                                cwd = cwd[dest]
                        elif rest == 'ls':
                            ls = True
                        else:
                            raise ValueError(f'{rest}: invalid command')
                    else:
                        if not ls:
                            raise ValueError(
                                'Encountered file listing outside of ls '
                                'command'
                            )
                        try:
                            size = int(id_)
                        except ValueError:
                            # This is a directory
                            cwd.mkdir(rest)
                        else:
                            # This is a file
                            cwd.add(rest, size=size)
            except StopIteration:
                pass

    def __getitem__(self, path: str) -> Directory|File:
        '''
        Return the desired Directory or File object
        '''
        try:
            return self.rootdir[path.lstrip(os.path.sep)]
        except FileNotFoundError as exc:
            raise FileNotFoundError(
                errno.ENOENT,
                os.strerror(errno.ENOENT),
                path,
            ) from exc

    @property
    def size(self) -> int:
        '''
        Return the size of the contents of the rootdir
        '''
        return self.rootdir.size

    @property
    def unused_size(self) -> int:
        '''
        Return the amount of unused space (disk space - size)
        '''
        ret = self.disk_size - self.size
        if ret < 0:
            raise OSError(errno.ENOSPC, os.strerror(errno.ENOSPC))
        return ret

    def dirs(self, recurse: bool = False) -> Iterator[Directory]:
        '''
        Generator function to return the directories within this directory
        '''
        return self.rootdir.dirs(recurse=recurse)

    def files(self, recurse: bool = False) -> Iterator[File]:
        '''
        Generator function to return the files within this directory
        '''
        return self.rootdir.files(recurse=recurse)


if __name__ == '__main__':
    aoc = AOC2022Day7()
    answer1 = 0
    for directory in aoc.dirs(recurse=True):
        dir_size = directory.size
        if dir_size <= 100_000:
            answer1 += dir_size
    print(f'Answer 1 (cumulative size of dirs <= 100000 bytes): {answer1}')

    target_unused = 30_000_000
    unused = aoc.unused_size
    excess_size = target_unused - unused
    if excess_size <= 0:
        sys.stderr.write(f'Unused space ({unused}) should be > target_unused\n')
        sys.exit(1)

    answer2 = min(
        size for size in (item.size for item in aoc.dirs(recurse=True))
        if size >= excess_size
    )
    print(f'Answer 2 (size of smallest dir to remove): {answer2}')
