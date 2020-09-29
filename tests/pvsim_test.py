# SPDX-License-Identifier: BSD-3-Clause

from pv_sim import pv_gen
import pv_sim
import unittest

import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


class PVGenTest(unittest.TestCase):

    def test_pvfile(self):
        pv_generator = pv_gen.PVGenerator(pv_gen.PVFile("../data/Jul2013.csv"))
        # Exact time
        value = pv_generator.gen_value(28800)
        self.assertEqual(value, 0.1257325)

        # Less than closest
        value = pv_generator.gen_value(28700)
        self.assertEqual(value, 0.1257325)

        # More than closest
        value = pv_generator.gen_value(28900)
        self.assertEqual(value, 0.1257325)
