#! /usr/bin/env python

__author__ = 'bbowman@pacificbiosciences.com'

from pbmgx.nucmer.coord import NucmerCoordReader
from pbmgx.nucmer.segment import Segment

MIN_LENGTH = 500
MIN_IDENTITY = 95.0

def read_segments( coord_file, min_length=MIN_LENGTH, min_identity=MIN_IDENTITY, remove_diag=True ):
    segments = []
    for hit in NucmerCoordReader( coord_file ):

        # Filter out low-quality hits before creating the Segment
        if (hit.E1 - hit.S1) < min_length:
            continue
        if hit.IDY < min_identity:
            continue
        if remove_diag and (hit.S1 == hit.S2 == 1) and \
                           (hit.E1 == hit.E2):
            continue

        # If the hit passed all filters, convert it to a Segment and keep it
        segment = Segment( hit.S1, hit.E1, hit.query )
        segments.append( segment )
    return segments

def sort_segments( segments, reverse=False ):
    segments = sorted( segments, key=len, reverse=not reverse )
    segments = sorted( segments, reverse=reverse )
    return segments

def remove_subset_segments( segments ):
    segments = sort_segments( segments )
    new_segments = []
    for segment in segments:
        if any([s.contains(segment) for s in new_segments]):
            continue
        new_segments.append( segment )
    return new_segments