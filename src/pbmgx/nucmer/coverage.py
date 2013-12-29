#! /usr/bin/env python

__author__ = 'bbowman@pacificbiosciences.com'

from pbmgx.nucmer.coord import NucmerCoordReader
from pbmgx.nucmer.segment import Segment
from pbcore.io import FastaReader

MIN_LEN = 10000

def calculate_coverage( coord_file, query_fasta, ref_fasta, min_length=MIN_LEN ):
    query_lengths = read_fasta_lengths( query_fasta )
    ref_lengths = read_fasta_lengths( ref_fasta )
    ref_windows = read_ref_segments( coord_file, min_length )
    print ref_windows
    segment_dict = combine_segments( ref_windows )
    gap_dict = find_coverage_gaps( segment_dict, ref_lengths )
    print segment_dict
    print gap_dict
    calculate_coverage_fraction( gap_dict, ref_lengths )

def calculate_coverage_fraction( gap_dict, ref_lengths ):
    for reference, gaps in gap_dict.iteritems():
        length = float(ref_lengths[reference])
        covered = [len(g) for g in gaps if g.source == 'covered']
        uncovered = [len(g) for g in gaps if g.source == 'uncovered']
        total = covered + uncovered
        print "Covered Gaps: {0}bp ({1:.2%}) from {2} gaps".format(sum(covered),
                                                                   sum(covered)/length,
                                                                   len(covered))
        print "Uncovered Gaps: {0}bp ({1:.2%}) from {2} gaps".format(sum(uncovered),
                                                                     sum(uncovered)/length,
                                                                     len(uncovered))
        print "Total Gaps: {0}bp ({1:.2%}) from {2} gaps".format(sum(total),
                                                                 sum(total)/length,
                                                                 len(total))

def find_coverage_gaps( segment_dict, lengths ):
    gap_dict = {}
    for reference, segments in segment_dict.iteritems():
        gap_dict[reference] = []

        prev_source = None
        prev_end = 0

        # Iterate through each Segment, checking for gaps between
        for segment in segments:
            if segment.start > prev_end + 1:
                if segment.source and segment.source == prev_source:
                    gap = Segment( prev_end+1, segment.start-1, 'covered' )
                else:
                    gap = Segment( prev_end+1, segment.start-1, 'uncovered' )
                gap_dict[reference].append( gap )
            prev_source = segment.source
            prev_end = segment.end

        # Check that the end of the segments is flush with the reference end
        length = lengths[reference]
        if prev_end < length:
            gap = Segment( prev_end+1, length, 'uncovered' )
            gap_dict[reference].append( gap )

    return gap_dict

def combine_segments( segment_dict ):
    new_segment_dict = {}
    for reference, segments in segment_dict.iteritems():
        new_segments = []
        for i, curr_seg in enumerate( segments ):
            # Find if curr_seg overlaps existing segments
            overlap_flag = False
            for other_seg in new_segments:
                if curr_seg.overlaps( other_seg ):
                    overlap_flag = True
                    break
            # if so it has already been incorporated and can be skipped
            if overlap_flag:
                continue

            # Otherwise, check it against the remaining segments
            for other_seg in segments[i+1:]:
                if curr_seg.overlaps( other_seg ) and curr_seg.source == other_seg.source:
                    curr_seg = curr_seg.combine( other_seg )

            # Add the maximized curr_seg to the output
            new_segments.append( curr_seg )
        new_segment_dict[reference] = sorted(new_segments)
    return new_segment_dict

def read_ref_segments( coord_file, min_length=MIN_LEN ):
    segments = {}
    for hit in NucmerCoordReader( coord_file ):
        segment = Segment( hit.S1, hit.E1, hit.query )
        if len(segment) < min_length:
            continue
        try:
            segments[hit.reference].append( segment )
        except:
            segments[hit.reference] = [ segment ]
    return segments

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