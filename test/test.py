#!/usr/bin/env python

import unittest
import subprocess
import shutil
import os
import sys

TOPDIR = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), '..'))

class Tests(utils.TestBase):
        # todo: assert outputs

class Tests(utils.TestBase):
    def test_Rrp6(self):
        """Test model building and analysis"""
        os.chdir(os.path.join(TOPDIR, 'sampling', 'modeling'))
        p = subprocess.check_call(["python", 'modeling.py', "--test"])
        # todo: assert outputs
        os.chdir(os.path.join(TOPDIR, 'analysis', 'clustering'))
        p = subprocess.check_call(["python", 'clustering.py'])
        p = subprocess.check_call(["python", 'high_confidence_structure.py'])
        p = subprocess.check_call(["python", 'precision_rmsf.py'])
        p = subprocess.check_call(["python", 'XL_table.py'])
        p = subprocess.check_call(["python", 'XL_table_tail.py'])
        p = subprocess.check_call(["python", 'XL_table_middle.py'])

if __name__ == '__main__':
    unittest.main()
