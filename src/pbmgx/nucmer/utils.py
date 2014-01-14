#! /usr/bin/env python

__author__ = 'bbowman@pacificbiosciences.com'

from pbmgx.nucmer.coord import NucmerCoordReader
from pbmgx.nucmer.snp import NucmerSnpReader

def read_nucmer_hits( nucmer_file, min_length=None, min_identity=None):
    hits = []
    for hit in NucmerCoordReader( nucmer_file ):
        if min_length and (hit.E1 - hit.S1) < min_length:
            continue
        if min_identity and hit.IDY < min_identity:
            continue
        hits.append( hit )
    return hits

def read_nucmer_snps( nucmer_file ):
    snps = []
    for snp in NucmerSnpReader( nucmer_file ):
        snps.append( snp )
    return snps

def is_self_nucmer_file( nucmer_file ):
    """
    Check whether a Nucmer file was run against itself
    """
    queries = set()
    references = set()
    for hit in NucmerCoordReader( nucmer_file ):
        queries.add( hit.query )
        references.add( hit.reference )
    return queries == references
