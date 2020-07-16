""" Main application entry point

    python -m varanus  ...
"""
import sys

import cliff.app
import cliff.commandmanager

from .__version__ import __version__
from .session import Session
from .__patch__ import apply_patch

CLINS = 'varanus.clier'


class VaranusApp(cliff.app.App):

    def __init__(self):
        super().__init__(
            description='varanus',
            version=__version__,
            command_manager=cliff.commandmanager.CommandManager(CLINS),
            deferred_help=True,
        )

    def initialize_app(self, argv):
        """The varanus application initialization

        This attaches a session to the application object.

        * ``varanus_session``
        """
        self.varanus_session = Session()
        self.LOG.debug(f'initialize_app() varanus_session: {self.varanus_session}')
        self.LOG.debug(f'initialize_app() config: {self.varanus_session.config}')

    def prepare_to_run_command(self, cmd):
        self.LOG.debug('prepare_to_run_command %s', cmd.__class__.__name__)

    def clean_up(self, cmd, result, err):
        self.LOG.debug('clean_up %s', cmd.__class__.__name__)
        if err:
            self.LOG.error('got an error: %s', err)


def main():
    """ Execute the application
    """
    app = VaranusApp()
    apply_patch(app)
    app.run(sys.argv[1:])


# Make the script runnable

if __name__ == "__main__":
    raise SystemExit(main())

