# -*- coding: UTF-8 -*-
"""
Created on 2016/6/2

@author: mavericks
"""

from app import create_app

application = create_app('production')

if __name__ == '__main__':
    application.run(host='0.0.0.0', port=5000, debug=True)
