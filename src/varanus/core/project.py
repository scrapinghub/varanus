"""Scrapinghub project access
"""
import logging
import cliff.hooks
import varanus.lib


class Project(cliff.hooks.CommandHook):
    """Project logic

    .. todo:: Perhaps we can remove `project` from parsed_args after
        attaching to session?
    """
    log = logging.getLogger(__name__)

    def get_parser(self, parser):
        return parser

    def get_epilog(self):
        pass

    def before(self, parsed_args):
        """Attach the project to the session

        parsed_args.project: int
        session.project    : scrapinghub.Project
        """
        session = self.cmd.app.varanus_session
        default_pid = session.config.default_project
        pid = getattr(parsed_args, 'project', None) or default_pid
        kwargs = parse_keyword_args(pid, parsed_args)
        project = varanus.lib.Project(session, **kwargs)
        if project is None:
            raise RuntimeError('No project specified')
        session.project = project

    def after(self, parsed_args, return_code):
        pass


def parse_keyword_args(project_id, parsed_args):
    """Parse the command line arguments into a dict

    Basically this function allows us to specify a *job key* or an
    *item key* on the command line and it will automatically also:

    * set the *project* parameter
    * set the *key* paramenter

    .. note:: The ``parsed_args`` argument might be mutated

    .. todo:: Make sure that the `project` (if also provided) matches the one in the keys
    """
    kwargs = dict(parsed_args._get_kwargs())
    p = project_id
    if kwargs.get('jobkey'):
        def keys():
            jobkeys = kwargs['jobkey']
            if isinstance(jobkeys, str):
                jobkeys = (jobkeys, )
            for key in jobkeys:
                key = key.strip('/')
                slashes = key.count('/')
                if slashes == num_components - 2:
                    kwargs['project'] = int(p)
                    yield f'{p}/{key}'
                elif slashes == num_components - 1:
                    kwargs['project'] = int(key.partition('/')[0])
                    yield key
                else:
                    raise RuntimeError(f'Key "{key}" should have {num_components} components')
        num_components = 3
        parsed_args.key = list(keys())
        kwargs.pop('jobkey')

    if kwargs.get('itemkey'):
        num_components = 4
        key = kwargs['itemkey'].strip('/')
        slashes = key.count('/')
        if slashes == num_components - 2:
            kwargs['project'] = int(p)
            kwargs['itemkey'] = f'{p}/{key}'
        elif slashes == num_components - 1:
            kwargs['project'] = int(key.partition('/')[0])
            kwargs['itemkey'] = key
        else:
            raise RuntimeError(f'Key "{key}" should have {num_components} components')
        parsed_args.itemkey = kwargs['itemkey']

    return kwargs
