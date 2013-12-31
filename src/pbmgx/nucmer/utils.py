#! /usr/bin/env python

__author__ = 'bbowman@pacificbiosciences.com'

from pbmgx.nucmer.coord import NucmerCoordReader

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