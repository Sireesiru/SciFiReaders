"""
Test of CZIReader
part of SciFiReaders a pycroscopy package
"""

import sys
import sidpy
import numpy as np
import urllib
import os
import unittest

sys.path.append("../../../../../SciFiReaders/")
import SciFiReaders

root_path = "https://github.com/pycroscopy/SciFiDatasets/blob/main/data/microscopy/em/tem/"


class TestCZI(unittest.TestCase):

    def test_czi_file(self):
        file_path = os.path.join(root_path, 'stains_first_1.1.czi?raw=true')
        file_name = 'stains_first_1.1.czi'
        urllib.request.urlretrieve(file_path, file_name)

        reader = SciFiReaders.CZIReader(file_name)
        datasets = reader.read()

        self.assertEqual(type(datasets), list)
        self.assertGreater(len(datasets), 0)

    def test_data_available(self):
        file_path = os.path.join(root_path, 'stains_first_1.1.czi?raw=true')
        file_name = 'stains_first_1.1.czi'
        urllib.request.urlretrieve(file_path, file_name)

        reader = SciFiReaders.CZIReader(file_name)

        self.assertIsInstance(reader, sidpy.Reader)

    def test_read_datasets(self):
        file_path = os.path.join(root_path, 'stains_first_1.1.czi?raw=true')
        file_name = 'stains_first_1.1.czi'
        urllib.request.urlretrieve(file_path, file_name)

        reader = SciFiReaders.CZIReader(file_name)
        datasets = reader.read()

        expected_labels_3d = ['channel_axis (index)', 'y_axis (m)', 'x_axis (m)']
        expected_labels_2d = ['y_axis (m)', 'x_axis (m)']

        for ind, dataset in enumerate(datasets):
            self.assertIsInstance(dataset, sidpy.Dataset)

            for axis_idx in range(dataset.ndim):
                self.assertIsInstance(dataset._axes[axis_idx], sidpy.Dimension)

            actual_labels = list(dataset.labels)
            if dataset.ndim == 3:
                self.assertEqual(actual_labels, expected_labels_3d)
            else:
                self.assertEqual(actual_labels, expected_labels_2d)

            self.assertIn('instrument', dataset.metadata)
            self.assertGreater(float(dataset.max()), float(dataset.min()))


if __name__ == '__main__':
    unittest.main()