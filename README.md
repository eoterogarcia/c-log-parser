# c-log-parser

Tool for parsing log files. Each log file contains newline-terminated, space-separated text formatted like:

`<unix_timestamp> <hostname> <hostname>`

For example:
```text
1366815793 quark garak
1366815795 brunt quark
1366815811 lilac garak
```
Each line represents connection from a host (left) to another host (right) at a given time. The lines are roughly sorted by timestamp. They might be out of order by maximum 5 minutes.

### Goals to Achieve

#### 1. Parse the data with a time_init, time_end
Given the name of a file (with the format described above), an init_datetime, an end_datetime, and a Hostname, returns: a list of hostnames connected to the given host during the given period

#### 2. Unlimited Input Parser
The tool should both parse previously written log files and terminate or collect input from a new log file while it's being written and run indefinitely.

The script will output, once every hour:
 - a list of hostnames connected to a given (configurable) host during the last hour
 - a list of hostnames received connections from a given (configurable) host during the last hour
 - the hostname that generated most connections in the last hour

Both the number of log lines and hostnames can be very high. Consider implementing a CPU and memory-efficient solution. Please feel free to make assumptions as necessary with proper documentation

### Installation

#### From source

Download the source code by cloning the repository or by pressing 'Download ZIP' on this page.

```shell script
python3 setup.py install
```

### Documentation

#### Command line usage
Run the following for information about options and arguments.
```shell script
> python3 src/start.py -h
usage: start.py [-h] --log_file LOG_FILE [--init_datetime INIT_DATETIME] [--end_datetime END_DATETIME] [--target_hostname TARGET_HOSTNAME] [--source_hostname SOURCE_HOSTNAME] [--output OUTPUT]

Log parser utility

optional arguments:
  -h, --help            show this help message and exit
  --log_file LOG_FILE   Path to the log file to parse
  --init_datetime INIT_DATETIME
                        Filter connections defining the initial datetime, format: "dd/mm/yyyy hh:mm:ss"
  --end_datetime END_DATETIME
                        Filter connections defining the end datetime, format: "dd/mm/yyyy hh:mm:ss"
  --target_hostname TARGET_HOSTNAME
                        Get a list of hostnames connected to a given configurable target hostname
  --source_hostname SOURCE_HOSTNAME
                        Get a list of hostnames received connections from a given configurable source hostname
  --output OUTPUT       Path of the output file to write parsed results. If not defined, results are printed in console
```
Disclaimer: `OUTPUT` parameter functionality not implemented yet.

##### Execution example
Log parsing to obtain the list of hostnames connected to "Dmetri" hostname and the list of hostnames connected from "Kishauna" hostname:
```shell script
python3 src/start.py --log_file test/data/input-file-10000.txt --source_hostname Kishauna --target_hostname Dmetri
```

Log parsing to obtain the list of hostnames connected to "Dmetri" during de the interval datetime defined:
```shell script
python3 src/start.py --log_file test/data/input-file-10000.txt --init_datetime "12/08/2019 21:00:00" --end_datetime "14/08/2019 23:00:00" --target_hostname Dmetri
```
