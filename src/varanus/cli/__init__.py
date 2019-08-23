"""Application command line interface
"""
from .job     import Job                 # noqa
from .jobs    import Jobs                # noqa
from .item    import Item                # noqa
from .stats   import Stats               # noqa
from .project import Project             # noqa
from .collect import Collections         # noqa
from .scripts import Workers as Scripts  # noqa
from .spiders import Workers as Spiders  # noqa
from .workers import Workers             # noqa

# Mutually exclusive parser group helper
# https://stackoverflow.com/questions/15008758#answer-31347222
# def add_bool_arg(parser, name, default=False):
#     group = parser.add_mutually_exclusive_group(required=False)
#     group.add_argument('--' + name, dest=name, action='store_true')
#     group.add_argument('--no-' + name, dest=name, action='store_false')
#     parser.set_defaults(**{name:default})
# add_bool_arg(parser, 'useful-feature')
# add_bool_arg(parser, 'even-more-useful-feature')
