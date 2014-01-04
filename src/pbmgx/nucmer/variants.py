#! /usr/bin/env python

__author__ = 'bbowman@pacificbiosciences.com'

from pbmgx.nucmer.utils import read_nucmer_snps
from pbmgx.fasta.utils import read_fastq_dict

def summarize_variants( snp_file, query_fastq ):
    snps = read_nucmer_snps( snp_file )
    records = read_fastq_dict( query_fastq )
    print records
    print len(snps)

if __name__ == '__main__':
    import sys

    snp_file = sys.argv[1]
    query_fastq = sys.argv[2]

    summarize_variants( snp_file, query_fastq )
