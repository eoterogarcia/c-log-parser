import argparse
from typing import Tuple, Generator
from datetime import datetime

from src.common.log_reader import LogReader


def get_args() -> Tuple[str, datetime, datetime, str, str]:
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
    parser.add_argument('--target_hostname', type=str, help='The target hostname ', required=True)
    parser.add_argument('--output', type=str, help='Path of the output file to write parsed results. If not defined, '
                                                   'results are printed in console', required=False)
    args = parser.parse_args()

    datetime_format = '%d/%m/%Y %H:%M:%S'
    parameters = (str(args.log_file), datetime.strptime(args.init_datetime, datetime_format),
                  datetime.strptime(args.end_datetime, datetime_format), str(args.target_hostname),
                  str(args.output) if args.output else None)
    return parameters


def get_source_host_list(reader_generator: Generator,
                         init_datetime: datetime,
                         end_datetime: datetime,
                         target_host: str,
                         output: str):
    for record in reader_generator:
        if init_datetime <= record[LogReader.TIMESTAMP_CONNECTION] <= end_datetime and target_host == record[LogReader.TARGET_HOST]:
            if output:
                # todo write results to file as soon as they are generated
                record[LogReader.SOURCE_HOST]
            else:
                print(record[LogReader.SOURCE_HOST])
        elif init_datetime > record[LogReader.TIMESTAMP_CONNECTION]:
            # time range passed, so abort log parser because lines are sorted by timestamp
            break


if __name__ == '__main__':
    file_path, time_init, time_end, target, output_file = get_args()

    log_reader = LogReader('test/data/tiny_log.txt')
    reader = log_reader.read_log_lines()
    get_source_host_list(reader, time_init, time_end, target, output_file)
