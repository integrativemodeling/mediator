#!/usr/bin/env python

import unittest
import subprocess
import shutil
import os
import sys
import ihm.reader

TOPDIR = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), '..'))

class Tests(unittest.TestCase):
    def test_simple(self):
        """Test model building and analysis"""
        os.chdir(os.path.join(TOPDIR, 'sampling', 'modeling'))
        p = subprocess.check_call(["python", 'modeling.py', "--test"])
        # todo: assert outputs
        os.chdir(os.path.join(TOPDIR, 'analysis', 'clustering'))
        # Back up pregenerated outputs (needed for mmCIF test)
        os.rename('kmeans_weight_500_4', 'pregen-outputs')
        p = subprocess.check_call(["python", 'clustering.py', '--test'])
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
        # Put back pregenerated outputs
        shutil.rmtree('kmeans_weight_500_4')
        os.rename('pregen-outputs', 'kmeans_weight_500_4')

    def test_mmcif(self):
        """Test generation of mmCIF output"""
        os.chdir(os.path.join(TOPDIR, 'sampling', 'modeling'))
        if os.path.exists("mediator.cif"):
            os.unlink("mediator.cif")
        p = subprocess.check_call(
                ["python", "modeling.py", "--mmcif", "--dry-run"])
        # Check output file
        self._check_mmcif_file('mediator.cif')

    def _check_mmcif_file(self, fname):
        with open(fname) as fh:
            s, = ihm.reader.read(fh)
        self.assertEqual(len(s.citations), 1)
        self.assertEqual(s.citations[0].doi, '10.7554/eLife.08719')
        self.assertEqual(len(s.software), 5)
        self.assertEqual(len(s.orphan_starting_models), 14)
        # Should be 4 models in a single state
        self.assertEqual(len(s.state_groups), 1)
        self.assertEqual(len(s.state_groups[0]), 1)
        self.assertEqual(len(s.state_groups[0][0]), 4)
        models = [g[0] for g in s.state_groups[0][0]]
        self.assertEqual([len(m._spheres) for m in models],
                         [2711, 2711, 2711, 2711])
        self.assertEqual([len(m._atoms) for m in models], [0, 0, 0, 0])
        # Should be 4 ensembles (clusters)
        self.assertEqual([e.num_models for e in s.ensembles],
                         [142, 192, 39, 126])
        # Check localization densities
        self.assertEqual([len(e.densities) for e in s.ensembles], [25]*4)
        self.assertEqual([len(e.sequence) for e in s.entities],
                         [295, 223, 115, 687, 307, 210, 121, 284, 222, 149,
                          127, 140, 157, 566, 1082, 220, 436, 401, 1146,
                          1094, 986])
        self.assertEqual([a.details for a in s.asym_units],
                         ['med6', 'med8', 'med11', 'med17', 'med18', 'med20',
                          'med22', 'med4', 'med7', 'med9', 'med31', 'med21',
                          'med10', 'med1', 'med14', 'med19', 'med2', 'med3',
                          'med5', 'med15', 'med16'])
        # One crosslink restraint and 2 EM3D restraints
        xl, em3d1, em3d2 = s.restraints
        self.assertEqual(len(xl.experimental_cross_links), 359)
        self.assertEqual(len(xl.cross_links), 359)
        self.assertEqual(xl.dataset.location.path,
                  'mediator-v1.0.3/sampling/CXMS_files/full_med_splitmods.txt')
        self.assertEqual(sum(len(x.fits) for x in xl.cross_links), 1436)

        self.assertEqual(len(em3d1.fits), 4)
        self.assertEqual(len(em3d2.fits), 4)
        self.assertEqual(em3d1.dataset.location.path,
                'mediator-v1.0.3/sampling/em_map_files/'
                'asturias_middle_module_translated_resampled.mrc.gmm.29.txt')
        parent = em3d1.dataset.parents[0].parents[0]
        self.assertEqual(parent.location.access_code, 'EMD-2634')


if __name__ == '__main__':
    unittest.main()
