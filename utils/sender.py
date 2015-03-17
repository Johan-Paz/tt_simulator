#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: japaz

from config import Environment
import httplib, urllib
from os import path
import yaml

def send_sequence(sequence,context=None,verbosity=False):
    seqfile = path.join(path.dirname(__file__),"..","samples",sequence + ".yaml")
    if not path.isfile(seqfile):
        print 'ERROR: no such samples/%s.yaml file.' % sequence
    else:
        with open(seqfile) as seq_yaml:
            seq_content = seq_yaml.read()
            list_measures = yaml.load(seq_content.replace('\t','   '))
            if list_measures:
                for step in list_measures:
                    step_in = context.recall(step['in'])
                    step_out = context.recall(step['out'])
                    success, out = send_measure(step_in,context)
                    assert success,'Failed the access to the server.'
                    assert step_out==out, "The expected answer is '%s' and '%s' is received." % (step_out,out)
                    if verbosity:
                        print 'SUCCESS: ' + step_in + ' --> '+ step_out


def send_measure(measure,context=None,verbosity=False):
    '''
    This function will send a line of measure towards the configured end-point
    '''
    try:
        if not context:
            context = Environment()
        end_point = context.get('southbound.end-point')
        port = context.get('southbound.port')
        url = context.get('southbound.url')

        if not end_point:
            return False, None

        server = end_point
        if port:
        	server += ':' + str(port)

        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        parameters = urllib.urlencode({'cadena':measure})

        connection = httplib.HTTPConnection(server)

        connection.request("POST",url,parameters,headers=headers)

        response = connection.getresponse()
        body = response.read()
        if verbosity:
            print response.status, body

        return True, body
    except Exception, e:
        if verbosity:
            print e
        return False, None
