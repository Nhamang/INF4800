#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import Iterator
from invertedindex import Posting


class PostingsMerger:
    """
    Utility class for merging posting lists.
    """

    @staticmethod
    def intersection(p1: Iterator[Posting], p2: Iterator[Posting]) -> Iterator[Posting]:
        """
        A generator that yields a simple AND of two posting lists, given
        iterators over these.

        The posting lists are assumed sorted in increasing order according
        to the document identifiers.

        raise NotImplementedError
        """

        a, b = next(p1, None), next(p2, None)
        while a is not None and b is not None:
            if a.document_id == b.document_id:
                yield(a)
                a, b = next(p1, None), next(p2, None)
            elif a.document_id > b.document_id:
                b = next(p2, None)
            elif a.document_id < b.document_id:
                a = next(p1, None)

    @staticmethod
    def union(p1: Iterator[Posting], p2: Iterator[Posting]) -> Iterator[Posting]:
        """
        A generator that yields a simple OR of two posting lists, given
        iterators over these.

        The posting lists are assumed sorted in increasing order according
        to the document identifiers.

        raise NotImplementedError
        """

        a, b = next(p1, None), next(p2, None)
        while a is not None and b is not None:
            if a.document_id == b.document_id:
                yield (a)
                a, b = next(p1, None), next(p2, None)
            elif a.document_id > b.document_id:
                yield (b)
                b = next(p2, None)
                if b is None:
                    while a is not None:
                        yield(a)
                        a = next(p1, None)
            elif a.document_id < b.document_id:
                yield (a)
                a = next(p1, None)
                if a is None:
                    while b is not None:
                        yield(b)
                        b = next(p2, None)

