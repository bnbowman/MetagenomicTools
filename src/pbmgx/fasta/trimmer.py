#! /usr/bin/env python

__author__ = 'bbowman@pacificbiosciences.com'

import re
from pbcore.io import (FastaRecord, FastaReader,
                       FastqRecord, FastqReader)
from pbmgx.fasta.utils import write_records, is_fasta, is_fastq

def trim_sequences( sequence_file ):
    if is_fasta( sequence_file ):
        trim_fasta( sequence_file )
    elif is_fastq( sequence_file ):
        trim_fastq( sequence_file )
    else:
        raise ValueError

def trim_fastq( fastq_file ):
    records = list( FastqReader( fastq_file ))
    records = [trim_fastq_record(r) for r in records]
    write_records( records, fastq_file )

def trim_fasta( fasta_file ):
    records = list( FastaReader( fasta_file ))
    records = [trim_fasta_record(r) for r in records]
    write_records( records, fasta_file )

def trim_fastq_record( record ):
    left_trimmed = re.sub('^[agct]+', '', record.sequence)
    left_trim = len(record.sequence) - len(left_trimmed)
    trimmed_seq = re.sub('[agct]+$', '', left_trimmed)
    right_trim = len(left_trimmed) - len(trimmed_seq)
    right_trim_start = len(record.sequence) - right_trim
    trimmed_qual = record.quality[left_trim:right_trim_start]
    print len(trimmed_seq)
    print len(trimmed_qual)
    return FastqRecord( record.name, trimmed_seq, trimmed_qual )

def trim_fasta_record( record ):
    sequence = re.sub('^[agct]+', '', record.sequence)
    sequence = re.sub('[agct]+$', '', sequence)
    return FastaRecord( record.name, sequence )

if __name__ == '__main__':
    import sys

    sequence_file = sys.argv[1]

    trim_sequences( sequence_file )
