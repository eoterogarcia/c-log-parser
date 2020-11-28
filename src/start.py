import argparse
from typing import Tuple, Generator
from datetime import datetime

from src.common.log_reader import LogReader


def get_args() -> Tuple[str, datetime, datetime, str]:
    """
    Get the execution arguments
    :return: Tuple with the values (kpi, levels, category, env, period, execution, personalized_period,
    country, input_method)
    """
    parser = argparse.ArgumentParser(description='Log parser utility')
    parser.add_argument('--log_file', type=str, help='Path to the log file', required=True)
    parser.add_argument('--init_datetime', type=str, help='Initial datetime connection, format: "dd/mm/yyyy hh:mm:ss"',
                        required=True)
    parser.add_argument('--end_datetime', type=str, help='End datetime connection, format: "dd/mm/yyyy hh:mm:ss"',
                        required=True)
    parser.add_argument('--target_hostname', type=str, help='', required=True)
    args = parser.parse_args()

    datetime_format = '%d/%m/%Y %H:%M:%S'
    return str(args.log_file), datetime.strptime(args.init_datetime, datetime_format), \
           datetime.strptime(args.end_datetime, datetime_format), str(args.target_hostname)


def get_source_host_list(reader_generator: Generator, init_datetime: datetime, end_datetime: datetime, target_host: str):
    source_host_list = []
    for record in reader_generator:
        if init_datetime <= record[LogReader.TIMESTAMP_CONNECTION] <= end_datetime and target_host == record[LogReader.TARGET_HOST]:
            source_host_list.append(record[LogReader.SOURCE_HOST])
            # todo change! write results to file as soon as they are generated
    return source_host_list


if __name__ == '__main__':
    file_path, init, end, target = get_args()

    log_reader = LogReader('test/data/tiny_log.txt')
    reader = log_reader.read_log_lines()
    host_list = get_source_host_list(reader, init, end, target)
    print(host_list)
