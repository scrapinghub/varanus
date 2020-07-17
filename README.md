# Varanus

This tool wraps an API POST request to scrapinghub's job and other data storage API.

## Requirements

- Python 3.6+
- Poetry

## Developer Notes

For those unfamiliar with poetry, it's a virtualenv + package manager.

The project originally was built to use it, but instead of beginning the `poetry new` command,  we do a hybrid clone + poetry install

(Since the project uses a `.lock` file, using pipenv plus some virtualenv manager should also work, but these instructions use poetry.)

### Install

    $ pip install poetry

    $ git clone https://github.com/scrapinghub/varanus.git

    $ cd varanus

When you install an application using poetry, a virtualenv is created automagically:

    $ poetry install

    Creating virtualenv varanus-mrejzrgU-py3.8 in /home/mns/.cache/pypoetry/virtualenvs

    Installing dependencies from lock file

    Package operations: 47 installs, 0 updates, 0 removals

      - Installing decorator (4.4.0)
      - Installing ipython-genutils (0.2.0)
      - Installing six (1.12.0)
      - Installing attrs (19.1.0)
      - Installing certifi (2019.6.16)
      - Installing chardet (3.0.4)
      - Installing idna (2.8)
      [ . . . snip . . . ]
      - Installing zipp (0.5.2)
      - Installing importlib-metadata (0.19)
      - Installing atomicwrites (1.3.0)
      - Installing more-itertools (7.2.0)
      - Installing pluggy (0.12.0)
      - Installing py (1.8.0)
      - Installing pytest (3.10.1)
      - Installing varanus (0.1.0)

### Usage

Example usage:

    $ poetry run varanus jobs -p 376566 -s dod_953_tripadvisor

    ●▬▬▬▬▬▬▬▬▬●   <Response [200]> https://storage.scrapinghub.com/jobq/376566/list?content=results&fit_width=False&formatter=table&max_width=0&noindent=False&print_empty=False&project=376566&quote_mode=nonnumeric&start=0&jobmeta=project&jobmeta=spider&jobmeta=spider_args&jobmeta=job_cmd&jobmeta=tags&jobmeta=scrapystats&jobmeta=units&jobmeta=version&jobmeta=priority&jobmeta=pending_time&jobmeta=running_time&jobmeta=finished_time&jobmeta=scheduled_by&jobmeta=state&jobmeta=close_reason&state=finished&spider=dod_953_tripadvisor&count=10 ●  varanus.__patch__:scrapinghub.client.HubstorageClient.request

    +----------------+---------------------+----------+----------+------------------+------------------+-----+-------+-------+--------+----------+----------+-----------------+
    | Key            | Spider              | Pnd mins | Run mins | Start            | Finish           | Err |  Warn | Items |  Pages | State    | Reason   | Version         |
    +================+=====================+==========+==========+==================+==================+=====+=======+=======+========+==========+==========+=================+
    | 376566/418/805 | dod_953_tripadvisor |        0 |        9 | 2020/04/19 19:10 | 2020/04/19 19:19 |   0 |    41 |    73 |    567 | finished | finished | 2233af50-master |
    +----------------+---------------------+----------+----------+------------------+------------------+-----+-------+-------+--------+----------+----------+-----------------+

#### Options

To see the command line arguments run varanus help:

    $ poetry run varanus help

    usage: varanus [--version] [-v | -q] [--log-file LOG_FILE] [-h] [--debug]

    optional arguments:
      --version            show program's version number and exit
      -v, --verbose        Increase verbosity of output. Can be repeated.
      -q, --quiet          Suppress output except warnings and errors.
      --log-file LOG_FILE  Specify a file to log output. Disabled by default.
      -h, --help           Show help message and exit.
      --debug              Show tracebacks on errors.

    Commands:
      collect        List project collections
      complete       print bash completion command (cliff)
      help           print detailed help for another command (cliff)
      item           List item attributes for a given key
      job            List job attributes for a given job key
      jobs           List jobs filtered by various options
      project        Show project attributes
      scripts        List the project scripts & spiders
      spiders        List the project scripts & spiders
      stats          Show jobs statistics
      workers        List the project scripts & spiders

You can also get help for individual commands:

    $ poetry run varanus jobs --help

    usage: varanus jobs [-h] [-f {csv,graph,json,table,value,yaml}] [-c COLUMN]
                        [--quote {all,minimal,none,nonnumeric}] [--noindent]
                        [--max-width <integer>] [--fit-width] [--print-empty]
                        [--sort-column SORT_COLUMN] [--project PROJECT]
                        [--spider SPIDER] [--key JOBKEY]
                        [--all-tags ALL_TAGS [ALL_TAGS ...]]
                        [--any-tags HAS_TAG [HAS_TAG ...]]
                        [--not-tags LACKS_TAG [LACKS_TAG ...]] [--arg WORKER_ARG]
                        [--count COUNT] [--start START] [--running]
                        [{all,args,codes,info,results,tags,time}]

    List jobs filtered by various options

    positional arguments:
      {all,args,codes,info,results,tags,time}
                            Job listing content

    optional arguments:
      -h, --help            show this help message and exit
      --project PROJECT, -p PROJECT
      --spider SPIDER, -s SPIDER
                            Filter for given spider name
      --key JOBKEY, -k JOBKEY
                            Job key, e.g. 123/456/789 or just 456/789
      --all-tags ALL_TAGS [ALL_TAGS ...], -t ALL_TAGS [ALL_TAGS ...]
                            Jobs have all of the tags
      --any-tags HAS_TAG [HAS_TAG ...]
                            Jobs have any of the tags
      --not-tags LACKS_TAG [LACKS_TAG ...]
                            Jobs do not have any of the tags
      --arg WORKER_ARG, -a WORKER_ARG
                            Filter for given argument
      --count COUNT         How many jobs show
      --start START         How many jobs to skip
      --running             Also show running jobs

    output formatters:
      output formatter options

      -f {csv,graph,json,table,value,yaml}, --format {csv,graph,json,table,value,yaml}
                            the output format, defaults to table
      -c COLUMN, --column COLUMN
                            specify the column(s) to include, can be repeated
      --sort-column SORT_COLUMN
                            specify the column(s) to sort the data (columns
                            specified first have a priority, non-existing columns
                            are ignored), can be repeated

    CSV Formatter:
      --quote {all,minimal,none,nonnumeric}
                            when to include quotes, defaults to nonnumeric

    json formatter:
      --noindent            whether to disable indenting the JSON

    table formatter:
      --max-width <integer>
                            Maximum display width, <1 to disable. You can also use
                            the CLIFF_MAX_TERM_WIDTH environment variable, but the
                            parameter takes precedence.
      --fit-width           Fit the table to the display width. Implied if --max-
                            width greater than 0. Set the environment variable
                            CLIFF_FIT_WIDTH=1 to always enable
      --print-empty         Print empty table if there is no data to show.

Also, take a look at the `add_argument` calls in
The varanus [CLI folder](https://github.com/scrapinghub/varanus/tree/master/src/varanus/cli).

#### Graph

You can use the Cliff output formatter to display data as a graph on an HTML page using `-f graph`:

    $ poetry run varanus jobs -f graph

![Job graph](https://user-images.githubusercontent.com/204645/87793796-bc75ec00-c813-11ea-8eed-8bd9d1e615cc.png)

### Debugging

There are a couple ways Cliff can assist in debugging.

#### Debug

Add the `--debug` command-line flag to set `app.options.debug` which you can reference in your program:

  $ poetry run varanus scripts --debug

Then in your code you can use it:

    if app.options.debug:
        log_response(response)

#### Verbosity

Set the `-v` flag to set the logging level:

  $ poetry run varanus scripts -vv

The log level is set depending on how many *v*'s you supply:

*  0: level = `warning` if you do not supply any
*  1: level = `info` if you supply one `-v`
*  2: level = `debug` if you supply two `-vv`
