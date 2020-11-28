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