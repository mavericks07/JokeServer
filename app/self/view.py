# -*- coding: UTF-8 -*-
"""
Created on 2016/6/5

@author: mavericks
"""
from flask import render_template
from . import self


@self.route('/')
def self():
    return render_template('self.html')