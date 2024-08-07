#!/usr/bin/env python
'''
https://adventofcode.com/2022/day/7
'''
from __future__ import annotations
import errno
import os
import re
import textwrap
from collections.abc import Iterator

# Local imports
from aoc import AOC


class PathBase:
    '''
    Base class for Directory and File objects
    '''
    def __init__(self, name: str, parent: Directory | None) -> None:
        '''
        Create an empty directory
        '''
        self.name: str = name
        self.parent: Directory | None = parent

    @property
    def parent(self) -> Directory | None:
        '''
        Return the parent directory
        '''
        return self.__parent

    @parent.setter
    def parent(self, value: Directory | None) -> None:
        '''
        Validate and set the parent
        '''
        if not (value is None or isinstance(value, Directory)):
            raise ValueError(
                f'Expected Directory or NoneType, not {type(value).__name__}'
            )
        self.__parent: Directory | None = value

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
        ptr: PathBase = self
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
                    yield from item.dirs(recurse=recurse)

    def files(self, recurse: bool = False) -> Iterator[File]:
        '''
        Generator function to return the files within this directory
        '''
        for item in self:
            if isinstance(item, File):
                yield item
            else:
                if recurse:
                    yield from item.files(recurse=recurse)


class AOC2022Day7(AOC):
    '''
    Day 7 of Advent of Code 2022
    '''
    example_data: str = textwrap.dedent(
        '''
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
        '''
    )

    validate_part1: int = 95437
    validate_part2: int = 24933642

    disk_size = 70_000_000

    # Set by post_init
    rootdir = None

    def post_init(self) -> None:
        '''
        Load the datastream
        '''
        self.rootdir: Directory = Directory('/')

        line_re: re.Pattern = re.compile(r'^(\$|\d+|dir) (.+)')
        ls: bool = False

        cwd: Directory = self.rootdir

        line: str
        for line in self.input.splitlines():
            id_: str
            rest: str
            id_, rest = line_re.match(line).groups()
            if id_ == '$':
                if rest.startswith('cd '):
                    dest: str = rest[3:]
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
                    size: int = int(id_)
                except ValueError:
                    # This is a directory
                    cwd.mkdir(rest)
                else:
                    # This is a file
                    cwd.add(rest, size=size)

    def __getitem__(self, path: str) -> Directory | File:
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
        ret: int = self.disk_size - self.size
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

    def part1(self) -> int:
        '''
        Calculate the cumulative size of dirs <= 100000 bytes in size
        '''
        size: int = 0
        directory: Directory
        for directory in self.dirs(recurse=True):
            dir_size: int = directory.size
            if dir_size <= 100_000:
                size += dir_size

        return size

    def part2(self) -> int:
        '''
        Calculate the size of the smallest dir that can be removed to bring the
        amount of unused space above the target
        '''
        target_unused: int = 30_000_000
        unused: int = self.unused_size
        excess_size: int = target_unused - unused
        if excess_size <= 0:
            raise RuntimeError(f'Unused space ({unused}) should be > {target_unused}')

        return min(
            size for size in (item.size for item in self.dirs(recurse=True))
            if size >= excess_size
        )


if __name__ == '__main__':
    aoc = AOC2022Day7()
    aoc.run()
