"""Gene Compair"""
# coding: utf-8
# fipylint: disable = C0103

import functools

@functools.total_ordering
class GenePair(object):
    """GenePair Class"""
    def __init__(self, f, gene):
        self.f = f
        self.gene = gene

    def __lt__(self, other):
        return {True: 1, False: -1}[self.f < other.f]

    def __eq__(self, other):
        return self.f == other.f
