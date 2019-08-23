"""Scrapinghub workers access
"""
import logging
import cliff.hooks
import varanus.lib


class Workers(cliff.hooks.CommandHook):
    """Workers logic
    """
    log = logging.getLogger(__name__)
    paths = ('scripts', 'spiders')

    def get_parser(self, parser):
        parser.conflict_handler = 'resolve'
        parser.add_argument('--sort-column', default='name')
        return parser

    def get_epilog(self):
        pass

    def before(self, parsed_args):
        """scrapinghub.Spiders glue to App
        """
        session = self.cmd.app.varanus_session
        kwargs = dict(parsed_args._get_kwargs())
        session.workers = varanus.lib.Workers(session, paths=self.paths, **kwargs)

    def after(self, parsed_args, return_code):
        pass
