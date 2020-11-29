import unittest
from datetime import datetime

from src.log_parser import get_source_host_list


class TestLogParser(unittest.TestCase):

    @staticmethod
    def create_reader_generator():
        records = [{'timestamp_conn': datetime.fromtimestamp(1565647204.351), 'source_host': 'Aadvik', 'target_host': 'Matina'},
                   {'timestamp_conn': datetime.fromtimestamp(1565647205.599), 'source_host': 'Keimy', 'target_host': 'Dmetri'},
                   {'timestamp_conn': datetime.fromtimestamp(1565647212.986), 'source_host': 'Tyreonna', 'target_host': 'Rehgan'},
                   {'timestamp_conn': datetime.fromtimestamp(1565647228.897), 'source_host': 'Heera', 'target_host': 'Eron'}]

        for record in records:
            yield record

    def setUp(self) -> None:
        self.reader = TestLogParser.create_reader_generator()

    def test_get_source_host_list_with_results(self):
        host_generator = get_source_host_list(self.reader,
                                              init_datetime=datetime(2019, 8, 12, 21, 0),
                                              end_datetime=datetime(2019, 8, 14, 21, 0),
                                              target_host='Dmetri')
        host_list = [host for host in host_generator]
        expected_host_list = ['Keimy']
        self.assertListEqual(host_list, expected_host_list, "Expected one host in list")

    def test_get_source_host_list_without_results(self):
        host_generator = get_source_host_list(self.reader,
                                              init_datetime=datetime(2019, 8, 12, 21, 0),
                                              end_datetime=datetime(2019, 8, 14, 21, 0),
                                              target_host='Zoheb')
        host_list = [host for host in host_generator]
        self.assertListEqual(host_list, [], "Expected zero host in list")
