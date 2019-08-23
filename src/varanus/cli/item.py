"""
+------------------+----------------------------------------------------
| Field            | Value                                             |
+------------------+----------------------------------------------------
| _id              | 48D1478A01EDDAC49ABB45C7E769C5E8D5CC6C49085C0294  |
| crawler          | Cb-suppertime                                     |
| team             | Cb                                                |
| timestamp_crawl  | 2019-06-04T14:23:16.514899Z                       |
| url              | https://example.net/                              |
| version          | 3.1                                               |
| content_type     | text/html; charset=utf-8                          |
| raw_content      | <!DOCTYPE html> <html lang="en"> <head> <meta char|
| response_headers | {'x-crawlera-slave': '107.183.168.12:4444'}       |
| objects          | []                                                |
| _type            | CXRItem                                           |
+------------------+----------------------------------------------------
"""
import logging
import cliff.show
import varanus.lib


class Item(cliff.show.ShowOne):
    """List item attributes for a given key
    """
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('itemkey', help='The item key, e.g. 123/456/789/0 or just 456/789/0')
        parser.add_argument('--project', '-p', type=int)
        return parser

    def take_action(self, parsed_args):
        session = self.app.varanus_session
        kwargs = dict(parsed_args._get_kwargs())
        item = varanus.lib.Item(session, **kwargs)
        return show_item(item)


def show_item(item):
    """
    ``item`` <class dict>::

        {'_id': '48D1478A01EDDAC49ABB45C7E769C5E8D5CC6C49085C0294',
         '_type': 'CXRItem',
         'content_type': 'text/html; charset=utf-8',
         'crawler': 'Cb-suppertime',
         'objects': [],
         'raw_content': '<!DOCTYPE html>\n</html>',
         'response_headers': {'x-crawlera-slave': '107.183.168.12'},
         'team': 'Cb',
         'timestamp_crawl': '2019-06-04T14:23:16.514899Z',
         'url': 'https://example.net/',
         'version': 3.1}
    """
    head = tuple(item.keys())
    body = tuple(item[k] for k in head)
    return (head, body)
