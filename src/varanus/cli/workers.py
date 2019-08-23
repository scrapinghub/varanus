"""
+----+----------------------------------------+
| Id | Name                                   |
+----+----------------------------------------+
|  0 | py:scripts                             |
|  0 | py:spiders                             |
|  0 | py:workers                             |
|  3 | arkansasrazorbacks.com_evenue          |
|  6 | byutickets.com_evenue                  |
|  8 | carnegiehall.org                       |
| 10 | centertheatregroup.org                 |
+----+----------------------------------------+

.. note:: A worker is either a spider or a script
"""
import logging
import cliff.lister


class Workers(cliff.lister.Lister):
    """List the project scripts & spiders
    """
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        # parser.formatter_class = argparse.ArgumentDefaultsHelpFormatter  # Show defaults
        parser.add_argument('--project', '-p', type=int)
        parser.add_argument('--recent', action='store_true', help='Retrieve most recent job data')
        parser.add_argument('--count', type=int, help='How many workers to show (default=10)', default=10)  # noqa
        parser.add_argument('--load', action='store_true', help='Retrieve all worker data like Id')
        archiv = parser.add_mutually_exclusive_group(required=False)
        archiv.add_argument('--both', dest='archived', action='store_const', help='Show both archived & current workers', const=None)  # noqa
        archiv.add_argument('--old', dest='archived', action='store_true', help='Show only archived workers')  # noqa
        archiv.add_argument('--no-old', dest='archived', action='store_false', help='Do not show any archived workers')  # noqa
        parser.set_defaults(archived=False)
        return parser

    def take_action(self, parsed_args):

        def headers():
            """Don't show certain columns if not requested"""
            yield from ('Id', 'Name', 'Archived')
            if parsed_args.recent:
                yield 'Recent'

        def fields(s):
            """Don't show certain columns if not requested"""
            yield from (s.jobq_id, s.name, s.archived)
            if parsed_args.recent:
                yield s.jobs

        head = tuple(headers())
        body = tuple(tuple(fields(s)) for s in self.app.varanus_session.workers)
        return (head, body)
