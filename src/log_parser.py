from typing import Generator
from datetime import datetime, timedelta
from src.common.log_reader import LogReader


def get_source_host_list(reader_generator: Generator,
                         init_datetime: datetime,
                         end_datetime: datetime,
                         target_host: str):
    hard_end_datetime = end_datetime + timedelta(minutes=5)
    for record in reader_generator:
        if init_datetime <= record[LogReader.TIMESTAMP_CONNECTION] <= end_datetime and target_host == record[LogReader.TARGET_HOST]:
            yield record[LogReader.SOURCE_HOST]
        elif hard_end_datetime < record[LogReader.TIMESTAMP_CONNECTION]:
            # time range passed, so abort log parser because lines are sorted by timestamp. Data can be
            # be out of order by maximum 5 minutes.
            break
