#! /usr/bin/env python

__author__ = 'Brett Bowman'
__email__ = 'bbowman@pacificbiosciences.com'

from pbmgx.io.BlasrIO import

def read_hits_by_query( blasr_file ):
    queries = {}
    for hit in BlasrReader( blasr_file ):
        try:
            queries[hit.qname].append( hit )
        except:
            queries[hit.qname] = [ hit ]
    return queries