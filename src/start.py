import argparse
from typing import Tuple
from datetime import datetime

from src.common.log_reader import LogReader
from src.log_parser import get_source_host_list


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


def process_log(input_path: str,
                init_datetime: datetime,
                end_datetime: datetime,
                target_host: str,
                output: str):
    log_reader = LogReader(input_path)
    reader = log_reader.read_log_lines()

    host_generator = get_source_host_list(reader, init_datetime, end_datetime, target_host)

    for host in host_generator:
        if not output:
            print(host)


if __name__ == '__main__':
    file_path, time_init, time_end, target, output_file = get_args()
    process_log(file_path, time_init, time_end, target, output_file)
