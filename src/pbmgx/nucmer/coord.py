#! /usr/bin/env python

__author__ = 'bbowman@pacificbiosciences.com'

from pbcore.io.base import ReaderBase

class NucmerHit( object ):
    """
    A Class for representing a Nucmer hit
    """

    def __init__(self, line):
        parts = line.strip().split()
        if len(parts) == 13:
            self.S1 = int(parts[0])
            self.E1 = int(parts[1])
            self.S2 = int(parts[3])
            self.E2 = int(parts[4])
            self.LEN1 = int(parts[6])
            self.LEN2 = int(parts[7])
            self.IDY = float(parts[9])
            self.reference = parts[11]
            self.query = parts[12]
        elif len(parts) == 9:
            self.S1 = int(parts[0])
            self.E1 = int(parts[1])
            self.S2 = int(parts[2])
            self.E2 = int(parts[3])
            self.LEN1 = int(parts[4])
            self.LEN2 = int(parts[5])
            self.IDY = float(parts[6])
            self.reference = parts[7]
            self.query = parts[8]
        else:
            raise ValueError("Invalid Nucmer Coordinate record")

class NucmerCoordReader( ReaderBase ):
    """
    A Class for reading Nucmer Coordinate files
    """

    def __iter__(self):
        try:
            parts = split_nucmer_coord_file(self.file)
            for line in parts:
                yield NucmerHit( line )
        except AssertionError:
            raise ValueError("Invalid Nucmer Coordinate file")



def split_nucmer_coord_file( handle ):
    """
    Split a nucmer coordinate file line-by-line, skipping any header rows
    """
    for line in handle:
        line = line.strip()
        if not line:
            continue
        if line.startswith('/') or line.startswith('NUCMER') or \
           line.startswith('[S1]') or line.startswith('==='):
            continue
        yield line