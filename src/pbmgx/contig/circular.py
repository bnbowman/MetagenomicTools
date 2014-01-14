#! /usr/bin/env python

__author__ = 'bbowman'

from pbmgx.fasta.utils import read_fasta_lengths
from pbmgx.io.utils import read_hits_by_query

def find_circularized_sequences( fasta_file, blasr_file ):
    lengths = read_fasta_lengths( fasta_file )
    hits = read_hits_by_query( blasr_file )
    filtered_hits = filter_hits( hits )

def filter_hits( blasr_hits ):
    print len(blasr_hits)
    hits = {q: v for q, v in blasr_hits.iteritems() if len(v) > 1}
    print len(hits)
    return hits

if __name__ == '__main__':
    import sys

    fasta_file = sys.argv[1]
    blasr_file = sys.argv[2]

    find_circularized_sequences( fasta_file, blasr_file )