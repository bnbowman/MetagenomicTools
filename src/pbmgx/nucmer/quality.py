#! /usr/bin/env python

from math import log10
from pbmgx.nucmer.utils import read_nucmer_snps

def calculate_quality( snp_file, enable_filter=True ):
    """
    Calculate the quality 
    """
    snps = read_nucmer_snps( snp_file )
    references = get_references( snps )
    queries = get_queries_by_ref( snps )
    lengths = get_sequence_lengths( snps )

    # Filter out SNPs where the reference is indeterminate
    if enable_filter:
        snps = filter_snps( snps )

    # Sort and summarize the remaining SNPs
    sorted_snps = sort_snps_by_query( snps )
    filtered_snps = filter_sorted_snps( sorted_snps )
    summarize_quality( filtered_snps, references, queries, lengths )

def calculate_qv( errors, total ):
    return int( -10 * log10( errors/float(total) ))

def calculate_per_mb( errors, total ):
    mb_ratio = total / 1000000.0
    return round(errors / mb_ratio, 1)

def format_summary(name, snps, length):
    qv = calculate_qv( snps, length )
    per_mb = calculate_per_mb( snps, length )
    return "{0}{1}\t{2}\t{3}\t{4}".format(name.ljust(32), 
                                          length, snps, 
                                          per_mb, qv)

def sort_sequences( seq_list, values ):
    return sorted( seq_list, key=lambda x: values[x], reverse=True )

def summarize_quality( sorted_snps, references, queries, lengths ):
    """
    Summarize the quality of each assembly by reference
    """
    print "{0}Length\tDiffs\tPerMb\tQV".format('Reference'.ljust(32))
    total_snps = 0
    total_length = 0
    for ref in sort_sequences( references, lengths ):
        ref_snps = 0
        ref_length = 0
        for contig in sort_sequences( queries[ref], lengths ):
        # Identify the relevant length and diff count
            length = lengths[contig]
            snps = len(sorted_snps[contig])
            # Add those values to the running totals
            ref_length += length
            ref_snps += snps
            print format_summary( contig, snps, length )
            # Calculate and report derived statistics
        total_snps += ref_snps
        total_length += ref_length
        print format_summary( ref, ref_snps, ref_length ), "\n"
    # Calculate and report a global accuracy summary
    total_qv = calculate_qv( total_snps, total_length )
    total_per_mb = calculate_per_mb( snps, length )
    print format_summary( "Total", total_snps, total_length )

def filter_sorted_snps( sorted_snps ):
    """
    Filter duplicate reference positions from sorted SNPS
    """
    filtered_snps = {}
    for ref, snps in sorted_snps.iteritems():
        filtered_snps[ref] = []
        pos = set()
        for snp in snps:
            if snp.P1 in pos:
                continue
            pos.add( snp.P1 )
            filtered_snps[ref].append( snp )
    return filtered_snps

def sort_snps_by_query( snp_list ):
    sorted_snps = {}
    for snp in snp_list:
        try:
            sorted_snps[snp.query].append( snp )
        except:
            sorted_snps[snp.query] = [ snp ]
    return sorted_snps

def get_references( snp_list ):
    references = set()
    [references.add(s.reference) for s in snp_list]
    return references

def get_queries_by_ref( snp_list ):
    queries = {}
    for snp in snp_list:
        try:
            queries[snp.reference].add( snp.query )
        except:
            queries[snp.reference] = set([ snp.query ])
    return queries

def filter_snps( snp_list ):
    """
    Filter out SNPs with an unknown/N for its reference
    """
    return [s for s in snp_list if s.S1 != 'N']

def get_sequence_lengths( snps ):
    lengths = {}
    for snp in snps:
        if snp.has_lengths:
            lengths[snp.reference] = snp.reference_length
            lengths[snp.query] = snp.query_length
        else:
            raise ValueError
    return lengths

if __name__ == '__main__':
    import sys

    snp_file = sys.argv[1]

    calculate_quality( snp_file, enable_filter=True )
