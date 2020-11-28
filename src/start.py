import argparse
from typing import Tuple
from datetime import datetime


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


if __name__ == '__main__':
    file_path, init_datetime, end_datetime, target_host = get_args()
