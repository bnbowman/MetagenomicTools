#! /usr/bin/env python

__author__ = 'bbowman@pacificbiosciences.com'

from pbcore.io import FastaWriter

def write_records( records, fasta_file ):
    with FastaWriter( fasta_file ) as handle:
        for record in records:
            handle.writeRecord( record )