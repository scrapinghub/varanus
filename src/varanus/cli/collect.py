"""
+------+------------------+
| Type | Name             |
+------+------------------+
| s    | check_jobs_store |
+------+------------------+

+-------------------+-----+--------------------------------------------+
| name              | id  | desc                                       |
+-------------------+-----+--------------------------------------------+
| py:spiders        | 101 | Show an id/name mapping for all spiders fo |
| py:run_manager.py | 103 | Start a CrawlManager to keep track of job  |
| py:jobs-scheduled | 105 | Show periodic jobs in a better format than |
| py:scripts        | 106 | Show an id/name mapping for all scripts fo |
| py:spiders-items  | 108 | Show recent scraped item counts for spider |
| py:states-count   | 109 | Show project jobs states: pending, running |
| py:states-graph   | 110 | Graph job state counts over time           |
| py:items-job      | 111 | Show scraped item data from Hubstorage     |
| py:items-job-sum  | 112 | Sum scraped item data for a job            |
| py:jobs-scheduler | 114 | Import/Export the Periodic Jobs in CSV for |
+-------------------+-----+--------------------------------------------+
"""
import json
import logging
import cliff.lister
import varanus.lib


class Collections(cliff.lister.Lister):
    """List project collections
    """
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('name', nargs='?', help='The name of the collection')
        parser.add_argument('--project', '-p', type=int)
        parser.add_argument('--write', help='Write a JSON string to collection')
        parser.add_argument('--count', type=int, default=10, help='How many collections to show')
        parser.add_argument('--filter', help='Filter by key=value (not related to _key)')
        parser.add_argument('--key', '-k', help='Filter by collection key')
        return parser

    def take_action(self, parsed_args):
        session = self.app.varanus_session

        # List all collections for project
        if parsed_args.name is None:
            return show_collections(session.project)

        # Write to collection
        if parsed_args.write:
            write_collection(session.project, parsed_args.name, parsed_args.write)

        # List items for named collection based on supplied filters
        kwargs = dict(parsed_args._get_kwargs())
        items = varanus.lib.CollectionItems(session, **kwargs)
        return show_collection(items)


def write_collection(project, name, json_string: str):
    collection_stream = project.collections.get_store(name).create_writer()
    collection_stream.write(json.loads(json_string))
    collection_stream.close()


def show_collection(items):
    """
    ``items`` <class 'generator'>::

        ({'_key': 'Job-299923-10-1',
          'checks': {'close_reason': {'completed_at': 1558360217303},
                     'delivery_check': {'completed_at': 1558360217303},
                     'url_item_count': {'completed_at': 1558360217303},
                     'log_alerts': {'completed_at': 1558360217303}}},
         {'_key': 'Job-299923-10-2',
          'checks': {'log_alerts': {'continuations': {
                        '1558446950806': {'next_start_offset': 243},
                        '1558447046620': {'next_start_offset': 327},
                        '1558447202316': {'next_start_offset': 327}}}}},
         {'_key': 'last_run-299923',
          'endts': 1558447202316,
          'jobkey': None,
          'startts': 1558447046620})
    """
    data = tuple(items)
    head = tuple({k for item in data for k in item.keys()})
    body = tuple(tuple(item.get(col) for col in head) for item in data)
    return (head, body)


def show_collections(project):
    """
    ``project``::

        <class 'scrapinghub.client.projects.Project'>
          ◇ _client       <scrapinghub.client.ScrapinghubClient>
          ◇ activity      <scrapinghub.client.activity.Activity>
          ◇ collections   <scrapinghub.client.collections.Collections>
          ◇ frontiers     <scrapinghub.client.frontiers.Frontiers>
          ◇ jobs          <scrapinghub.client.jobs.Jobs>
          ◇ key           '299923'
          ◇ settings      <scrapinghub.client.projects.Settings>
          ◇ spiders       <scrapinghub.client.spiders.Spiders>
    """
    head = ('Type', 'Name')
    body = tuple((c['type'], c['name']) for c in project.collections.iter())
    return (head, body)
