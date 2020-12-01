import argparse
from typing import Tuple
from datetime import datetime

from src.common.log_reader import LogReader
from src.log_parser import get_source_host_list, analyze_stream_log


def get_args() -> Tuple[str, datetime, datetime, str, str]:
    """
    Get the execution arguments
    :return: Tuple with the values (kpi, levels, category, env, period, execution, personalized_period,
    country, input_method)
    """
    parser = argparse.ArgumentParser(description='Log parser utility')
    parser.add_argument('--log_file', type=str, help='Path to the log file to parse', required=True)
    parser.add_argument('--init_datetime', type=str,
                        help='Filter connections defining the initial datetime, format: "dd/mm/yyyy hh:mm:ss"',
                        required=False)
    parser.add_argument('--end_datetime', type=str,
                        help='Filter connections defining the end datetime, format: "dd/mm/yyyy hh:mm:ss"',
                        required=False)
    parser.add_argument('--target_hostname', type=str,
                        help='Get a list of hostnames connected to a given configurable target hostname',
                        required=False)
    parser.add_argument('--source_hostname', type=str,
                        help='Get a list of hostnames received connections from a given configurable source hostname',
                        required=False)
    parser.add_argument('--output', type=str,
                        help='Path of the output file to write parsed results. If not defined, results are printed in console',
                        required=False)
    args = parser.parse_args()

    datetime_format = '%d/%m/%Y %H:%M:%S'
    parameters = (str(args.log_file),
                  datetime.strptime(args.init_datetime, datetime_format) if args.init_datetime else None,
                  datetime.strptime(args.end_datetime, datetime_format) if args.end_datetime else None,
                  str(args.source_hostname) if args.source_hostname else None,
                  str(args.target_hostname) if args.target_hostname else None,
                  str(args.output) if args.output else None)
    return parameters


def process_log(input_path: str,
                init_datetime: datetime,
                end_datetime: datetime,
                source_host: str,
                target_host: str,
                output: str):
    log_reader = LogReader(input_path)
    reader = log_reader.read_log_lines()

    if init_datetime and end_datetime and target_host:
        host_generator = get_source_host_list(reader, init_datetime, end_datetime, target_host)
        for host in host_generator:
            if not output:
                print(host)
    else:
        analyze_stream_log(reader, target_host, source_host, elapsed_time=60, unit_time_minutes=True)


if __name__ == '__main__':
    file_path, time_init, time_end, source, target, output_file = get_args()
    process_log(file_path, time_init, time_end, source, target, output_file)
