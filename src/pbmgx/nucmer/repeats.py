#! /usr/bin/env python

__author__ = 'bbowman@pacificbiosciences.com'

from pbmgx.nucmer.utils import read_segments

MIN_GENOME = 100000
MIN_REPEAT = 500
MIN_IDENTITY = 95.0

def summarize_repeats( coord_file, min_repeat=MIN_REPEAT, min_identity=MIN_IDENTITY ):
    segments = read_segments( coord_file, min_repeat, min_identity )

if __name__ == '__main__':
    import sys

    coord_input = sys.argv[1]

    summarize_repeats( coord_input )