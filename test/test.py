#!/usr/bin/env python

import unittest
import subprocess
import shutil
import os
import sys

TOPDIR = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), '..'))

class Tests(unittest.TestCase):
    def test_simple(self):
        """Test model building and analysis"""
        os.chdir(os.path.join(TOPDIR, 'sampling', 'modeling'))
        p = subprocess.check_call(["python", 'modeling.py', "--test"])
        # todo: assert outputs
        os.chdir(os.path.join(TOPDIR, 'analysis', 'clustering'))
        # Remove pregenerated outputs
        shutil.rmtree('kmeans_weight_500_4')
        p = subprocess.check_call(["python", 'clustering.py'])
        p = subprocess.check_call(["python", 'precision_rmsf.py', '--test'])
        p = subprocess.check_call(["python", 'XL_table.py'])
        p = subprocess.check_call(["python", 'XL_table_tail.py'])
        p = subprocess.check_call(["python", 'XL_table_middle.py'])
        # Assert that outputs were generated
        os.unlink('kmeans_weight_500_4/cluster.0/XL_table.pdf')
        os.unlink('kmeans_weight_500_4/cluster.0/XL_table_middle.pdf')
        os.unlink('kmeans_weight_500_4/cluster.0/XL_table_tail.pdf')
        os.unlink('kmeans_weight_500_4/cluster.0/rmsf.med15.dat')
        os.unlink('kmeans_weight_500_4/cluster.0/rmsf.med15.pdf')

if __name__ == '__main__':
    unittest.main()
