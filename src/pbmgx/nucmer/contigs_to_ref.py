#! /usr/bin/env python

from pbmgx.fasta.utils import read_fasta_lengths
from pbmgx.nucmer.utils import read_nucmer_hits

FRAC = 0.99

def contigs_to_refs( c_fasta, r_fasta, coord_file ):
    c_lengths = read_fasta_lengths( c_fasta )
    r_lengths = read_fasta_lengths( r_fasta )
    contigs = parse_contig_hits( coord_file )
    pick_contigs( c_lengths, r_lengths, contigs )

def parse_contig_hits( coord_file ):
    contigs = {}
    for hit in read_nucmer_hits( coord_file ):
        try:
            contigs[hit.reference].add( hit.query )
        except:
            contigs[hit.reference] = set([ hit.query ])
    return contigs

def pick_contigs( c_lengths, r_lengths, contigs ):
    for ref, size in r_lengths.iteritems():
        try:
            matches = contigs[ref]
        except:
            continue
        pick_contigs_for_ref( ref, size, matches, c_lengths )

def pick_contigs_for_ref( ref, size, matches, c_lengths ):
    assembly_size = 0
    used_contigs = []
    while assembly_size < size*FRAC:
        if len(matches) == 0:
            break
        max_size = max([c_lengths[m] for m in matches])
        max_contig = [m for m in matches if c_lengths[m] == max_size][0]
        assembly_size += max_size
        used_contigs.append( max_contig )
        matches = [m for m in matches if m != max_contig]
    print ref, size, assembly_size, len(used_contigs), ','.join( used_contigs )

if __name__ == '__main__':
    import sys

    c_fasta = sys.argv[1]
    r_fasta = sys.argv[2]
    coord_file = sys.argv[3]

    contigs_to_refs( c_fasta, r_fasta, coord_file )
