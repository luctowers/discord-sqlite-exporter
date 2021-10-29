# Discord SQLITE Exporter

A command line tool written in python to export discord text channels into relational SQLITE format.

## Schema

See [schema/setup.sql](schema/setup.sql)

## Usage

```
$ python3 src/main.py -h
usage: main.py [-h] -t TOKEN [-b] [-c CHANNELS [CHANNELS ...]] -d DATABASE [-l LIMIT]

Export discord chat logs to a Sqlite database.

optional arguments:
  -h, --help            show this help message and exit
  -t TOKEN, --token TOKEN
                        Discord access token
  -b, --bot             Enable if using a bot token
  -c CHANNELS [CHANNELS ...], --channels CHANNELS [CHANNELS ...]
                        Discord channel id(s)
  -d DATABASE, --database DATABASE
                        Sqlite database path
  -l LIMIT, --limit LIMIT
                        Maximum number of messages to consume from channels
```
