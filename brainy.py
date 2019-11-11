#!/usr/bin/env python3
# convert markdown file to thebrain plain thought format with out attachments here
'''
importing
	Child1
		- child 1 notes
	Child2
		# Grandson1
		Grandson2
	Grandson1
'''
import re
import sys

# nodes={'content', 'n|N|1'}
nodes = {'content', 'n|N|1'}
with open(sys.argv[1], mode='r') as f:
    lines = f.readlines()
    count_space = None
    for n in len(lines):
        gaps = re.search(r'(^(\s|\t)+?)[^\s\t]', lines[n]).group(1)
        if not count_space:
            count_space = len(gaps)
        lines[n] = ''.join(['\t'] * (gaps / count_space))
