import unittest
from src.common.log_reader import LogReader


class TestLogReader(unittest.TestCase):

    def setUp(self) -> None:
        self.log_reader = LogReader('test/data/tiny_log.txt')

    def test_read_log_lines(self):
        reader = self.log_reader.read_log_lines()
        records = []
        for record in reader:
            records.append(record)

        expected_records = [{'timestamp_conn': '1565647204351', 'source_host': 'Aadvik', 'target_host': 'Matina'},
                            {'timestamp_conn': '1565647205599', 'source_host': 'Keimy', 'target_host': 'Dmetri'},
                            {'timestamp_conn': '1565647212986', 'source_host': 'Tyreonna', 'target_host': 'Rehgan'},
                            {'timestamp_conn': '1565647228897', 'source_host': 'Heera', 'target_host': 'Eron'}]
        self.assertListEqual(expected_records, records)
