#! /usr/bin/env python

__author__ = 'bbowman@pacificbiosciences.com'

from pbmgx.nucmer.coord import NucmerCoordReader
from pbmgx.nucmer.utils import read_nucmer_hits
from pbmgx.nucmer.segment import Segment
from pbmgx.fasta.utils import read_fasta_lengths

MIN_LEN = 10000
MIN_IDY = 98.0
MARGIN = 5

def calculate_coverage( coord_file, query_fasta, ref_fasta, min_length=MIN_LEN,
                                                            min_identity=MIN_IDY,
                                                            margin=MARGIN ):
    query_lengths = read_fasta_lengths( query_fasta )
    ref_lengths = read_fasta_lengths( ref_fasta )
    nucmer_hits = read_nucmer_hits( coord_file, min_length, min_identity )
    segment_dict = nucmer_hits_to_segments( nucmer_hits )
    segment_dict = combine_segments( segment_dict )
    gap_dict = find_coverage_gaps( segment_dict, ref_lengths )
    print gap_dict
    gap_dict = mark_terminal_gaps( gap_dict, nucmer_hits, query_lengths, margin=margin)
    print gap_dict
    calculate_coverage_fraction( gap_dict, ref_lengths )
    #print locations

def mark_terminal_gaps( gap_dict, nucmer_hits, query_lengths, margin=MARGIN ):
    """
    Remove locations that appear to correspond to end-of-contig trimmings
    """
    filtered_gaps = {}
    for reference, gaps in gap_dict.iteritems():
        filtered_gaps[reference] = []
        for gap in gaps:
            length = query_lengths[gap.source]
            source = find_gap_source( gap, nucmer_hits )
            if is_terminal_gap( source, length, margin ):
                gap = Segment(gap.start, gap.end, 'uncovered')
            filtered_gaps[reference].append( gap )
    return filtered_gaps

def find_gap_source( gap, nucmer_hits ):
    start, end = None, None
    for hit in nucmer_hits:
        if gap.start == hit.E1+1:
            start = hit.E2
        if gap.end == hit.S1-1:
            end = hit.S2
    return sorted([start, end])

def is_terminal_gap( source, length, margin=MARGIN ):
    if source[0] <= margin and source[1] >= length-margin:
        return True
    return False

def calculate_coverage_fraction( gap_dict, ref_lengths ):
    for reference, gaps in gap_dict.iteritems():
        length = float(ref_lengths[reference])
        uncovered = [len(g) for g in gaps if g.source == 'uncovered']
        covered = [len(g) for g in gaps if g.source != 'uncovered']
        total = covered + uncovered
        print
        print "Covered Gaps: {0}bp ({1:.2%}) from {2} gaps".format(sum(covered),
                                                                   sum(covered)/length,
                                                                   len(covered))
        print covered
        print "Uncovered Gaps: {0}bp ({1:.2%}) from {2} gaps".format(sum(uncovered),
                                                                     sum(uncovered)/length,
                                                                     len(uncovered))
        print uncovered
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
                    gap = Segment( prev_end+1, segment.start-1, segment.source )
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

def nucmer_hits_to_segments( nucmer_hits ):
    segments = {}
    for hit in nucmer_hits:
        segment = Segment( hit.S1, hit.E1, hit.query )
        try:
            segments[hit.reference].append( segment )
        except:
            segments[hit.reference] = [ segment ]
    return segments

if __name__ == '__main__':
    import sys

    coord_file = sys.argv[1]
    query_fasta = sys.argv[2]
    ref_fasta = sys.argv[3]

    calculate_coverage( coord_file, query_fasta, ref_fasta )
