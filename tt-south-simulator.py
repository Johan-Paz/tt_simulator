#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: japaz
from lib.config import Environment
import lib.sender as sender
from os import path,walk
import sys

def execute_sequence(sequence,context,verbosity):
	print "Executing the sequence:", sequence
	sender.send_sequence(sequence,context,verbosity)

def execute_all_in(origin,context,verbosity):
	for dirname, dirnames, filenames in walk(origin):
	    # print path to all filenames.
	    for filename in filenames:
	    	if filename.endswith('.yaml'):
	    		execute_sequence(filename[:-5],context,verbosity)

doall = False
verbosity = False
environment = 'default'
sequence = None

num_param = len(sys.argv)
if num_param < 2:
    print "Usage: python tt-south-simulator.py [--V] [--environment] all|name-sequence"
else:
	for i in range(1,num_param):
		arg = sys.argv[i]
		if arg == 'all':
			doall = True
		elif arg == '--V':
			verbosity = True
		elif arg.startswith('--'):
			environment = arg[2:]
		else:
			sequence = arg

context = Environment(path.join(path.dirname(__file__),"conf","environment.yaml"),environment,True)

if not doall and not sequence:
	print "ERROR: no sequence to execute selected."
	sys.exit(1)

if not doall:
	execute_sequence(sequence,context,verbosity)
else:
	source = path.join(path.dirname(__file__),"samples")
	execute_all_in(source,context,verbosity)

