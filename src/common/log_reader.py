import csv


class LogReader(object):

    def __init__(self, file_path: str, read_options: str = 'r'):
        self.file_path = file_path
        self.read_options = read_options

    def read_log_lines(self):
        with open(self.file_path, self.read_options, newline='') as csvfile:
            reader = csv.DictReader(csvfile,
                                    fieldnames=['timestamp_conn', 'source_host', 'target_host'],
                                    delimiter=' ',
                                    quoting=csv.QUOTE_NONE)
            for record in reader:
                yield record
