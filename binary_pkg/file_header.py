# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function, unicode_literals)

MAXLENGTH = 1024


ELF_MAGIC = b'\x7fELF'

MACHO_MAGIC = frozenset([
    b'\xCA\xFE\xBA\xBE',  # Mach-O Fat Binary
    b'\xFE\xED\xFA\xCE',  # Mach-O binary (32-bit)
    b'\xFE\xED\xFA\xCF',  # Mach-O binary (64-bit)
    b'\xCE\xFA\xED\xFE',  # Mach-O binary (reverse byte ordering scheme, 32-bit)
    b'\xCF\xFA\xED\xFE',  # Mach-O binary (reverse byte ordering scheme, 64-bit)
])


class FileHeader(object):
    
    def __init__(self, path):
        self._path = path
        with open(path, 'rb') as f:
            self._head = f.read(MAXLENGTH)

    @property
    def head(self):
        return self._head

    def is_elf(self):
        return self.head[:4] == ELF_MAGIC

    def is_macho(self):
        return any(self.head.startswith(magic) for magic in MACHO_MAGIC)

    def is_binary(self):
        return self.is_elf() or self.is_macho()
