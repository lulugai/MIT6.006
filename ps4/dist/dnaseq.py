#!/usr/bin/env python2.7

import unittest
from dnaseqlib import *

### Utility classes ###

# Maps integer keys to a set of arbitrary values.
class Multidict:
    # Initializes a new multi-value dictionary, and adds any key-value
    # 2-tuples in the iterable sequence pairs to the data structure.
    def __init__(self, pairs=[]):
        # raise Exception("Not implemented!")
        self.dic = {}
        for pair in pairs:
            self.put(pair[0], pair[1])
    # Associates the value v with the key k.
    def put(self, k, v):
        # raise Exception("Not implemented!")
        if k in self.dic:
            self.dic[k].append(v)
        else:
            self.dic[k] = [v]

    # Gets any values that have been associated with the key k; or, if
    # none have been, returns an empty sequence.
    def get(self, k):
        # raise Exception("Not implemented!")
        try:
            return self.dic[k]
        except KeyError:
            return []

# Given a sequence of nucleotides, return all k-length subsequences
# and their hashes.  (What else do you need to know about each
# subsequence?)
def subsequenceHashes(seq, k):
    # raise Exception("Not implemented!")
    try:
        assert k > 0
        subseq = ''
        for i in range(0, k):
            subseq += seq.next()
        rh = RollingHash(subseq)
        pos = 0
        while True:
            yield (rh.current_hash(), (pos, subseq))
            previtm = subseq[0]
            subseq = subseq[1:] + seq.next()
            rh.slide(previtm, subseq[-1:])
            pos += 1
    except StopIteration:
        return
# Similar to subsequenceHashes(), but returns one k-length subsequence
# every m nucleotides.  (This will be useful when you try to use two
# whole data files.)
def intervalSubsequenceHashes(seq, k, m):
    try:
        assert m >= k
        pos = 0
        while True:
            subseq = ''
            for i in range(0, k):
                subseq += seq.next()
            rh = RollingHash(subseq)
            yield (rh.current_hash(), (pos, subseq))
            for j in range(m-k):
                seq.next()
            pos += m
    except StopIteration:
        return

# Searches for commonalities between sequences a and b by comparing
# subsequences of length k.  The sequences a and b should be iterators
# that return nucleotides.  The table is built by computing one hash
# every m nucleotides (for m >= k).
def getExactSubmatches(a, b, k, m):
    # a_hashval, (a_pos, a_subseq) = subsequenceHashes(a, k)
    seqtable = Multidict(intervalSubsequenceHashes(a, k, m))
    for b_hashval, (b_pos, b_subseq) in subsequenceHashes(b, k):
        for a_pos, a_subseq in seqtable.get(b_hashval):
            if a_subseq != b_subseq:
                continue
                # print(b_hashval, (a_pos, a_subseq))
            yield (a_pos, b_pos)
    return

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print ('Usage: {0} [file_a.fa] [file_b.fa] [output.png]'.format(sys.argv[0]))
        sys.exit(1)

    # The arguments are, in order: 1) Your getExactSubmatches
    # function, 2) the filename to which the image should be written,
    # 3) a tuple giving the width and height of the image, 4) the
    # filename of sequence A, 5) the filename of sequence B, 6) k, the
    # subsequence size, and 7) m, the sampling interval for sequence
    # A.
    compareSequences(getExactSubmatches, sys.argv[3], (500,500), sys.argv[1], sys.argv[2], 8, 100)
