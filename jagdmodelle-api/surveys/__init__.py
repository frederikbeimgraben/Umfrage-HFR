#!/usr/bin/env python3
"""
Load every .py file in this directory
"""

import os
import importlib

base_path = os.path.dirname(__file__)

for file in os.listdir(base_path):
    if file.endswith('.py') and not file.startswith('__'):
        importlib.import_module(f'.{file[:-3]}', 'surveys')
        