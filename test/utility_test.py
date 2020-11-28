import datetime
import unittest
import argparse
from unittest import mock
from datetime import datetime

from src.start import get_args


class TestParserArguments(unittest.TestCase):

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(log_file="test/data/tiny_log.txt",
                                                init_datetime="12/08/2019 21:00:00",
                                                end_datetime="12/08/2019 23:00:00",
                                                target_hostname="Dmetri"))
    def test_get_args(self, mock_args):
        file_path, init_datetime, end_datetime, target_host = get_args()
        self.assertEqual(file_path, "test/data/tiny_log.txt", "File path not equal")
        self.assertEqual(init_datetime, datetime(2019, 8, 12, 21, 0), "Init time not equal")
        self.assertEqual(end_datetime, datetime(2019, 8, 12, 23, 0), "End time not equal")
        self.assertEqual(target_host, "Dmetri", "Host not equal")
