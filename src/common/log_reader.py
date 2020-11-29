import csv
from datetime import datetime


class LogReader(object):

    TIMESTAMP_CONNECTION = 'timestamp_conn'
    SOURCE_HOST = 'source_host'
    TARGET_HOST = 'target_host'

    def __init__(self, file_path: str, read_options: str = 'r'):
        """
        Basic log reader constructor
        :param file_path: the path to the log file
        :param read_options: default is read only
        """
        self.file_path = file_path
        self.read_options = read_options

    def read_log_lines(self):
        """
        Read line by line
        :return a formatted log line as a dict
        :rtype: dict
        """
        with open(self.file_path, self.read_options, newline='') as csvfile:
            reader = csv.DictReader(csvfile,
                                    fieldnames=[LogReader.TIMESTAMP_CONNECTION, LogReader.SOURCE_HOST, LogReader.TARGET_HOST],
                                    delimiter=' ',
                                    quoting=csv.QUOTE_NONE)
            for record in reader:
                record[LogReader.TIMESTAMP_CONNECTION] = datetime.fromtimestamp(float(record[LogReader.TIMESTAMP_CONNECTION])/1000.0)
                yield record
