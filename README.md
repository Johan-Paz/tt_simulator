# Thinking Things Simulator. Introduction

A Thinking Thing simulator. Allow to create test to check the correctness of an Southbound Thinking Things end-point implementation.

In the current state only contains a python script that allow to run the sequences in the 'samples' directory and check the answers expected.

# Installation

The easiest way to obtain the simulator is to do a clone of this project with:

  git clone git@github.com:Johan-Paz/tt_simulator.git

# Basic configuration

The configuration file it is conf/environment.yaml and should contain at least the yaml:

  default:
  	southbound:
  		end-point: <IP address>
  		port: <port>
  		url: /Stack/Receive/

Where:

* <IP address>: it is the IP address of the southbound server to be tested
* <port>: the TCP port of the southbound server to be tested

With only this two parameter (plus the fixed url) the test can run the tests:

# Running the tester:

The tester is simply a Python program. When it is run without parameter it explains the parameters required and optional by itself:

  >> python tt-south-simulator.py
  Usage: python tt-south-simulator.py [--V] [--environment] all|name-sequence
  
The parameters are:

* --V: optional, activate the verbose mode, that explains all the test while running them. If it is not included, the scirpt only shows the failures.
* other -- paramater are interpreted as the name of one of the enviroment described in the file conf/environment.yaml, if it is not included 'default' it is selected
* 'all' or a name of a sequence in 'samples' directory.

# Samples

Each sample to be tested it is a .yaml file with a list of 'in-out', couples with the sintax:

  - in: '#<:identifier:>,#0,GM,m,34,0$'
    out: '#0,GM,m,34,-1$None,'
  - in: '#<:identifier:>,#0,GC,c,yes,0$,'
    out: '#0,GC,c,yes,-1$None,'
  - in: '#<:identifier:>,#0,GM,m,34,0$,#0,GC,c,yes,0$,'
    out: '#0,GM,m,34,-1$None,#0,GC,c,yes,-1$None,'

Any word surrounded by '<:' and ':>' are considered a token and it will be substituted by the value in the enviroment selected in conf/environment.yaml, like:

  default:
	  southbound:
		  end-point: 127.0.0.1
		  port: 8000
		  url: /Stack/Receive/
	  identifier: 8934071179000001899
	  
It is important to see that the lines in the samples need to be surronded by apostrophe like in the sample above.

# Advanced configuration

It is possible to include not only diferents enviroments but a enviroment selection in the configuration file, like in:

  environment: development
  development:
	  southbound:
		  end-point: 127.0.0.1
		  port: 8000
		  url: /Stack/Receive/
	  identifier: 8934071179000001899
  default:
	  southbound:
		  end-point: 127.0.0.1
		  port: 8000
	  	url: /Stack/Receive/
	  identifier: 8934071179000001899
