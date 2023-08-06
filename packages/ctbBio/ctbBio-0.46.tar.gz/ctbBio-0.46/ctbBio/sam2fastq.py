#!/usr/bin/env python3

"""
convert sam file to fastq file
"""

import sys
import os

# ctb
from ctbBio.rc import reverse_complement as rc

def print_single(line, rev):
    """
    print single reads to stderr
    """
    if rev is True:
        seq = rc(['', line[9]])[1]
        qual = line[10][::-1]
    else:
        seq = line[9]
        qual = line[10]
    fq = ['@%s' % line[0], seq, '+%s' % line[0], qual]
    print('\n'.join(fq), file = sys.stderr)

def sam2fastq(sam, singles = False, force = False):
    """
    convert sam to fastq
    """
    L, R = None, None
    for line in sam:
        if line.startswith('@') is True:
            continue
        line = line.strip().split()
        bit = [True if i == '1' else False \
                for i in bin(int(line[1])).split('b')[1][::-1]]
        while len(bit) < 8:
            bit.append(False)
        pair, proper, na, nap, rev, mrev, left, right = bit
        # make sure read is paired
        if pair is False:
            if singles is True:
                print_single(line, rev)
            continue
        # check if sequence is reverse-complemented
        if rev is True:
            seq = rc(['', line[9]])[1]
            qual = line[10][::-1]
        else:
            seq = line[9]
            qual = line[10]
        # check if read is forward or reverse, return when both have been found
        if left is True:
            if L is not None and force is False:
                print('sam file is not sorted', file = sys.stderr)
                print('\te.g.: %s' % (line[0]), file = sys.stderr)
                exit()
            if L is not None:
                L = None
                continue
            L = ['@%s' % line[0], seq, '+%s' % line[0], qual]
            if R is not None:
                yield L
                yield R
                L, R = None, None
        if right is True:
            if R is not None and force is False:
                print('sam file is not sorted', file = sys.stderr)
                print('\te.g.: %s' % (line[0]), file = sys.stderr)
                exit()
            if R is not None:
                R = None
                continue
            R = ['@%s' % line[0], seq, '+%s' % line[0], qual]
            if L is not None:
                yield L
                yield R
                L, R = None, None

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('usage: sam2fastq.py <mapping.sam> <singles to stderr?: True or False> <force exclude unpaired paired reads: True or False)>',
                file = sys.stderr)
        exit()
    sam, singles, force = sys.argv[1], sys.argv[2], sys.argv[3]
    if sam == '-':
        sam = sys.stdin
    else:
        sam = open(sam)
    if singles == 'True':
        singles = True
    else:
        singles = False
    if force == 'True':
        force = True
    else:
        force = False
    for seq in sam2fastq(sam, singles, force):
        print('\n'.join(seq))
