#! /usr/bin/env python

__author__ = 'bbowman@pacificbiosciences.com'

from pbcore.io.base import ReaderBase

class NucmerSnp( object ):
    """
    A Class for representing a Nucmer SNP
    """
    def __init__(self, line):
        parts = line.strip().split()
        parts = [p for p in parts if p != '|']
        if len(parts) == 10:
            self.P1 = int(parts[0])
            self.S1 = parts[1]
            self.S2 = parts[2]
            self.P2 = int(parts[3])
            self.BUFF = int(parts[4])
            self.DIST = int(parts[5])
            self.reference_length = None
            self.query_length = None
            self.reference = parts[8]
            self.query = parts[9]
        elif len(parts) == 12:
            self.P1 = int(parts[0])
            self.S1 = parts[1]
            self.S2 = parts[2]
            self.P2 = int(parts[3])
            self.BUFF = int(parts[4])
            self.DIST = int(parts[5])
            self.reference_length = int(parts[6])
            self.query_length = int(parts[7])
            self.reference = parts[10]
            self.query = parts[11]
        else:
            raise ValueError("Invalid Nucmer SNP record")

    def has_lengths(self):
        return (self.reference_length is not None and
                self.query_length is not None)

class NucmerSnpReader( ReaderBase ):
    """
    A Class for reading Nucmer Coordinate files
    """

    def __iter__(self):
        try:
            parts = split_nucmer_snp_file(self.file)
            for line in parts:
                yield NucmerSnp( line )
        except AssertionError:
            raise ValueError("Invalid Nucmer Coordinate file")



def split_nucmer_snp_file( handle ):
    """
    Split a nucmer coordinate file line-by-line, skipping any header rows
    """
    for line in handle:
        line = line.strip()
        if not line:
            continue
        if line.startswith('/') or line.startswith('NUCMER') or \
           line.startswith('[P1]') or line.startswith('==='):
            continue
        yield line
