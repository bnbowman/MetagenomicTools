#! /usr/bin/env python

__author__ = 'bbowman@pacificbiosciences.com'

import re
from pbcore.io import FastaRecord, FastaReader
from pbmgx.fasta.util import write_records

def trim_fasta( fasta_file ):
    records = list( FastaReader( fasta_file ))
    records = [trim_record(r) for r in records]
    write_records( records, fasta_file )

def trim_record( record ):
    sequence = re.sub('^[agct]+', '', record.sequence)
    sequence = re.sub('[agct]+$', '', sequence)
    return FastaRecord( record.name, sequence )

if __name__ == '__main__':
    import sys

    fasta_input = sys.argv[1]

    trim_fasta( fasta_input )