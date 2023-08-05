import os
import shutil
import unittest
from datetime import datetime
from multiprocessing import Process
from time import sleep

import numpy as np

import fasvautil as fu

SEQUENCE_NAME = 'test'

GPSLocation = fu.location.GPSLocation(position=(53.35131, 7.1933))


def update(q):
    for i in range(100):
        q.update_progress(i, 100)

        sleep(0.01)


class TqdmTest(unittest.TestCase):

    def setUp(self):
        self.manager = fu.io.TqdmManager()

    def test_1client(self):
        queue = self.manager.connect()

        self.manager.start()

        p = Process(target=update, args=(queue,))
        p.start()
        p.join()

    def test_2clients(self):
        queue1 = self.manager.connect()
        queue2 = self.manager.connect()

        self.manager.start()

        p1 = Process(target=update, args=(queue1,))
        p2 = Process(target=update, args=(queue2,))

        p1.start()
        p2.start()

        p1.join()
        p2.join()

    def tearDown(self) -> None:
        self.manager.stop()


class DataDirTest(unittest.TestCase):

    def test_update_data_dir(self):
        data_dir = os.getcwd()

        fu.io.set_data_dir(data_dir)

        # test directory in the data directory
        self.assertEqual(os.path.join(data_dir, 'test'), fu.io.data_dir('test'))

    def test_update_date_dir_and_write_numpy(self):
        data_dir = os.getcwd()
        fu.io.set_data_dir(data_dir)

        tstamp = datetime.now()
        file = os.path.join(data_dir, 'test', fu.io.format_datetime(tstamp) + ".npy")

        fpath = fu.io.save_ndarray(np.ones(3), tstamp, fu.io.data_dir('test'))

        self.assertEqual(file, fpath)

        self.assertTrue(os.path.isfile(file))

        shutil.rmtree(fu.io.data_dir('test'))
