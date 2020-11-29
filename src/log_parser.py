import time
from typing import Generator
from datetime import datetime, timedelta
from src.common import TIMESTAMP_CONNECTION, SOURCE_HOST, TARGET_HOST


def get_source_host_list(reader_generator: Generator,
                         init_datetime: datetime,
                         end_datetime: datetime,
                         target_host: str):
    """
    Given a log file, an init_datetime, an end_datetime, and a hostname, returns: a list of hostnames
    connected to the given host during the given period.
    :param reader_generator: file reader generator
    :param init_datetime: init datetime
    :param end_datetime: end datetime
    :param target_host: name of the target host
    """
    hard_end_datetime = end_datetime + timedelta(minutes=5)
    for record in reader_generator:
        if init_datetime <= record[TIMESTAMP_CONNECTION] <= end_datetime and target_host == record[TARGET_HOST]:
            yield record[SOURCE_HOST]
        elif hard_end_datetime < record[TIMESTAMP_CONNECTION]:
            # time range passed, so abort log parser because lines are sorted by timestamp. Data can be
            # be out of order by maximum 5 minutes.
            break


def _sum_connections(connections_host: dict, hostname: str):
    """
    Sum the connections for each hostname
    :param connections_host: dict with hostname as key and connections count as value
    :param hostname: needed to add a new connection to the count dict
    :return: updated dictionary
    """
    if hostname in connections_host:
        connections_host[hostname] += 1
    else:
        connections_host[hostname] = 1
    return connections_host


def _get_host_with_more_connections(connections_host: dict):
    """
    Sort dictionary with the connection count for each hostname in the time period.
    :param connections_host:
    :return: hostname with the highest number of connections
    """
    sorted_connections_host = sorted(connections_host.items(), key=lambda x: x[1], reverse=True)
    # todo get only the first connections
    return sorted_connections_host[0]


def _print_or_store_metrics(current_time: float, source: str, target_hosts: list,  target: str, source_hosts: list,
                            connections_host: dict):
    """
    Print or store values in a file (future feature)
    :param current_time:
    :param source:
    :param source_hosts:
    :param target:
    :param target_hosts:
    :param connections_host:
    """
    print(f"Metrics obtained at {current_time}")
    if target:
        print(f"Source hostnames connected to {target}: {source_hosts}")
    if source:
        print(f"Target hostnames connected from {source}: {target_hosts}")
    print(f"Hostname that generated most connections {_get_host_with_more_connections(connections_host)}")


def analyze_stream_log(reader_generator: Generator, target_host: str, source_host: str, elapsed_time: int = 60,
                       unit_time_minutes: bool = True):
    """
    Analyze and parse log file in streaming mode: once every the elapsed_time, function measures:
    - the list of hostnames connected to a given target_host, if target_host is not None
    - the list of hostnames received connections from a given source_host, if source_host is not None
    - the hostname that generated most connections
    :param reader_generator:
    :param target_host:
    :param source_host:
    :param elapsed_time: metrics are calculated every the elapsed_time is passed. Time unit is defined in minutes,
    otherwise change argument unit_time_minutes to False to consider time un seconds
    :param unit_time_minutes: Default True, if False, elapsed_time is expected to be in seconds
    """
    source_host_list = []
    target_host_list = []
    connections_host_count = {}

    elapsed_time_sec = float(elapsed_time * 60) if unit_time_minutes else float(elapsed_time)
    init_time = time.time()

    for record in reader_generator:
        current_time = time.time()
        if current_time - init_time >= elapsed_time_sec:
            # print/store values and ...
            _print_or_store_metrics(current_time, source_host, target_host_list, target_host, source_host_list,
                                    connections_host_count)
            # reset counters and timer
            source_host_list = []
            target_host_list = []
            connections_host_count = {}
            init_time = time.time()
        else:
            # count connections from source host
            connections_host_count = _sum_connections(connections_host_count, record[SOURCE_HOST])
            # evaluate conditions
            if target_host is not None and target_host == record[TARGET_HOST]:
                source_host_list.append(record[SOURCE_HOST])
            if source_host is not None and source_host == record[SOURCE_HOST]:
                target_host_list.append(record[TARGET_HOST])

    # print residual results
    _print_or_store_metrics(current_time, source_host, target_host_list, target_host, source_host_list,
                            connections_host_count)
