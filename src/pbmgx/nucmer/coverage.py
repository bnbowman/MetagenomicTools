#! /usr/bin/env python

__author__ = 'bbowman@pacificbiosciences.com'

from pbmgx.nucmer.coord import NucmerCoordReader
from pbcore.io import FastaReader

MIN_LEN = 10000

def calculate_coverage( coord_file, query_fasta, ref_fasta, min_length=MIN_LEN ):
    query_lengths = read_fasta_lengths( query_fasta )
    ref_lengths = read_fasta_lengths( ref_fasta )
    ref_windows = read_ref_windows( coord_file, min_length )
    print ref_windows
    print query_lengths
    print ref_lengths
    combine_windows( ref_windows )

def combine_windows( window_dict ):
    for reference, windows in window_dict.iteritems():
        for i, wi in enumerate(windows):
            for wj in windows[i+1:]:
                print wi, wj

def read_ref_windows( coord_file, min_length=MIN_LEN ):
    windows = {}
    for hit in NucmerCoordReader( coord_file ):
        if abs(hit.S1 - hit.E1) < min_length:
            continue
        try:
            windows[hit.reference].append( (hit.S1, hit.E1) )
        except:
            windows[hit.reference] = [ (hit.S1, hit.E1) ]
    return windows

def read_fasta_lengths( fasta_file ):
    lengths = {}
    for record in FastaReader( fasta_file ):
        name = record.name.strip().split()[0]
        lengths[name] = len( record.sequence )
    return lengths

if __name__ == '__main__':
    import sys

    coord_file = sys.argv[1]
    query_fasta = sys.argv[2]
    ref_fasta = sys.argv[3]

    calculate_coverage( coord_file, query_fasta, ref_fasta )