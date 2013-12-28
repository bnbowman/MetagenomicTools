#! /usr/bin/env python

__author__ = 'bbowman@pacificbiosciences.com'

class Segment( object ):
    """
    A Class for representing a segment of a Nucmer Alignment
    """

    def __init__(self, start, end):
        assert isinstance(start, int)
        assert isinstance(end, int)
        assert start != end
        self._start = start
        self._end = end

        if self.start > self.end:
            self._forward = True
        elif self.end > self.start:
            self._forward = False

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

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

    def overlap(self, other):
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
        assert self.overlap( other )
        if self.forward:
            start = min( self.start, other.start )
            end = max( self.end, other.end )
        else:
            start = max( self.start, other.start )
            end = min( self.end, other.end )
        return Segment( start, end )