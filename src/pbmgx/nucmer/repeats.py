#! /usr/bin/env python

__author__ = 'bbowman@pacificbiosciences.com'

from pbmgx.segment.utils import read_segments, remove_subset_segments
from pbmgx.nucmer.utils import is_self_nucmer_file

# Default filters for what constitutes a repeat
MIN_REPEAT = 500
MIN_IDENTITY = 95.0

# Default cut-offs for the different repeat classes
CLASS_III_CUTOFF = 7000
CLASS_II_CUTOFF = 100

def summarize_repeats( repeat_file, min_repeat=MIN_REPEAT, min_identity=MIN_IDENTITY ):
    """
    Summarize the repeats in a self-self coordinate file
    """
    assert is_self_nucmer_file( repeat_file )
    repeats = read_segments( repeat_file, min_repeat, min_identity )
    repeats = remove_subset_segments( repeats )
    report_repeats( repeats )


def report_repeats( repeats ):
    """
    Report the key stats of a set of repeats
    """
    # Summarize the remaining repeats
    max_repeat = max([len(r) for r in repeats])
    repeat_count = len( repeats )
    repeat_class = classify_repeats( repeats )
    print "Max Repeat Size: {0}".format( max_repeat )
    print "Number of Repeats: {0}".format( repeat_count )
    print "Repeat Class: {0}".format( repeat_class )


def classify_repeats( repeats ):
    """
    Summarize the repeat classification of a dataset
    """
    # Throw an error if no repeats given
    if len(repeats) == 0:
        raise ValueError("No repeats to ")

    max_repeat = max([len(r) for r in repeats])
    repeat_count = len(repeats)

    if max_repeat > CLASS_III_CUTOFF:
        return "III"
    elif repeat_count > CLASS_II_CUTOFF:
        return "II"
    return "I"

if __name__ == '__main__':
    import sys

    repeat_input = sys.argv[1]

    summarize_repeats( repeat_input )