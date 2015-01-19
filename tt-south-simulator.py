#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: japaz
from lib.config import Environment
from os import path

context = Environment(path.join(path.dirname(__file__),"conf","environment.yaml"))


