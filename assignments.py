#!/usr/bin/python
# -*- coding: utf-8 -*-

from normalization import BrainDeadNormalizer
from tokenization import BrainDeadTokenizer
from corpus import Document, InMemoryCorpus
from invertedindex import InMemoryInvertedIndex
from traversal import PostingsMerger
import re
import sys

def assignment_a():

    # Use these throughout below.
    normalizer = BrainDeadNormalizer()
    tokenizer = BrainDeadTokenizer()

    # Dump postings for a dummy two-document corpus.
    corpus = InMemoryCorpus()
    corpus.add_document(Document(0, {"body": "this is a Test"}))
    corpus.add_document(Document(1, {"body": "test TEST prØve"}))
    index = InMemoryInvertedIndex(corpus, ["body"], normalizer, tokenizer)
    for (term, expected) in zip(index.get_terms("PRøvE wtf tesT"), [[(1, 1)], [], [(0, 1), (1, 2)]]):
        print("***", term)
        assert term in ["prøve", "wtf", "test"]
        postings = list(index.get_postings_iterator(term))
        for posting in postings:
            print(posting)
        assert len(postings) == len(expected)
        assert [(p.document_id, p.term_frequency) for p in postings] == expected
    print(index)

    # Again, for a slightly bigger corpus.
    corpus = InMemoryCorpus("data/mesh.txt")
    index = InMemoryInvertedIndex(corpus, ["body"], normalizer, tokenizer)
    for (term, expected_length) in [("hydrogen", 8),
                                    ("hydrocephalus", 2)]:
        print("***", term)
        for posting in index.get_postings_iterator(term):
            print(posting)
        assert len(list(index.get_postings_iterator(term))) == expected_length

    # Test that we merge posting lists correctly. Note implicit test for case- and whitespace robustness.
    merger = PostingsMerger()
    and_query = ("HIV  pROtein", "AND", [11316, 11319, 11320, 11321])
    or_query = ("water Toxic", "OR", [3078, 8138, 8635, 9379, 14472, 18572, 23234, 23985] + [i for i in range(25265, 25282)])
    for (query, operator, expected_document_ids) in [and_query, or_query]:
        print(re.sub("\W+", " " + operator + " ", query))
        terms = index.get_terms(query)
        assert len(terms) == 2
        postings = [corpus.get_document(posting.document_id) for posting in {"AND": merger.intersection, "OR": merger.union}[operator](index.get_postings_iterator(terms[0]), index.get_postings_iterator(terms[1]))]
        print(*postings, sep = "\n")
        assert len(postings) == len(expected_document_ids)
        assert [posting.document_id for posting in postings] == expected_document_ids

def assignment_b():
    pass

def assignment_c():
    pass

def assignment_d():
    pass

def assignment_e():
    pass

if __name__ == "__main__":
    tests = {"a": assignment_a,
             "b": assignment_b,
             "c": assignment_c,
             "d": assignment_d,
             "e": assignment_e}
    assignments = sys.argv[1:] or tests.keys()
    for assignment in assignments:
        print("*** ASSIGNMENT", assignment.upper(), "***")
        tests[assignment.lower()]()
    print("*************************")
    print("*** ALL TESTS PASSED! ***")
    print("*************************")
