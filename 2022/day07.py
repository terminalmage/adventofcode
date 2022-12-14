#!/usr/bin/env python
'''
https://adventofcode.com/2022/day/7
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
    Base class for Day 7 of Advent of Code 2022
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
