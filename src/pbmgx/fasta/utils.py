#! /usr/bin/env python

__author__ = 'bbowman@pacificbiosciences.com'

from pbcore.io import (FastaWriter, FastaReader, FastaRecord, 
                       FastqWriter, FastqReader, FastqRecord)

def write_records( records, filename ):
    if is_fasta( filename ):
        write_fasta_records( records, filename )
    elif is_fastq( filename ):
        write_fastq_records( records, filename )
    else:
        raise ValueError

def write_fastq_records( records, filename ):
    with FastqWriter( filename ) as handle:
        for record in records:
            assert isinstance( record, FastqRecord )
            handle.writeRecord( record )

def write_fasta_records( records, filename ):
    with FastaWriter( filename ) as handle:
        for record in records:
            assert isinstance( record, FastaRecord )
            handle.writeRecord( record )

def read_fasta_lengths( fasta_file ):
    lengths = {}
    for record in FastaReader( fasta_file ):
        name = record.name.strip().split()[0]
        lengths[name] = len( record.sequence )
    return lengths

def read_fastq_dict( fastq_file ):
    records = {}
    for record in FastqReader( fastq_file ):
        name = record.name.strip().split()[0]
        records[name] = record
    return records

def is_fasta( filename ):
    return filename.endswith('.fa') or filename.endswith('.fasta')

def is_fastq( filename ):
    return filename.endswith('.fq') or filename.endswith('.fastq')
