#! /usr/bin/env python

__author__ = 'bbowman@pacificbiosciences.com'

from pbmgx.segment.segment import Segment

class SegmentPair( object ):
    """
    A Class for representing a segment of a Nucmer Alignment
    """

    def __init__(self, reference, query):
        assert isinstance(reference, Segment)
        assert isinstance(query, Segment)
        self._reference = reference
        self._query = query

        if self.reference.forward == self.query.forward:
            self._orientation = 'same'
        else:
            self._orientation = 'opposite'

    @property
    def reference(self):
        return self._reference

    @property
    def query(self):
        return self._query

    @property
    def orientation(self):
        return self._orientation