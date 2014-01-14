#! /usr/bin/env python

__author__ = 'bbowman@pacificbiosciences.com'

class Segment( object ):
    """
    A Class for representing a segment of a Nucmer Alignment
    """

    def __init__(self, start, end, source=None):
        assert isinstance(start, int)
        assert isinstance(end, int)
        assert start != end
        self._start = start
        self._end = end
        self._source = source

        if self.start < self.end:
            self._forward = True
        elif self.start > self.end:
            self._forward = False

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    @property
    def source(self):
        return self._source

    @property
    def leftmost(self):
        return min(self.start, self.end)

    @property
    def rightmost(self):
        return max(self.start, self.end)

    @property
    def forward(self):
        return self._forward

    @property
    def reverse(self):
        return not self._forward

    @property
    def orientation(self):
        if self.forward:
            return 'forward'
        elif self.reverse:
            return 'reverse'

    def __len__(self):
        return abs(self.start - self.end)

    def __repr__(self):
        return '<Segment: {0}-{1} from {2}>'.format(self.start, self.end, self.source)

    def __lt__(self, other):
        assert isinstance(other, Segment)
        return self.leftmost < other.leftmost

    def __gt__(self, other):
        assert isinstance(other, Segment)
        return self.leftmost > other.leftmost

    def overlaps(self, other):
        assert isinstance( other, Segment )
        if self.orientation != other.orientation:
            return False
        if other.end >= self.end >= other.start:
            return True
        elif other.end >= self.start >= other.start:
            return True
        return False

    def combine(self, other):
        assert isinstance( other, Segment )
        assert self.overlaps( other )
        if self.forward:
            start = min( self.start, other.start )
            end = max( self.end, other.end )
        else:
            start = max( self.start, other.start )
            end = min( self.end, other.end )

        # Maintain the Source if shared, otherwise discard
        if self.source == other.source:
            return Segment( start, end, self.source )
        return Segment( start, end )

    def contains(self, other):
        assert isinstance(other, Segment)
        if (self.leftmost <= other.leftmost) and \
           (self.rightmost >= other.rightmost):
            return True
        return False

    def is_contained_by(self, other):
        assert isinstance(other, Segment)
        return other.contains( self )