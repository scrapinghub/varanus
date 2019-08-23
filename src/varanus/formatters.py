"""Output formatters
"""
import plotly
import plotly.graph_objs as go

from cliff.formatters.base import ListFormatter, SingleFormatter


class GraphFormatter(ListFormatter, SingleFormatter):
    """Output formatter for graphs
    """

    def add_argument_group(self, parser):
        # group = parser.add_argument_group(title='graph formatter')
        # group.add_argument(
        #     '--save',
        #     action='store_true',
        #     help='whether to disable indenting the JSON'
        # )
        pass

    def emit_list(self, column_names, data, stdout, parsed_args):
        """Create HTML file with interactive graph

        ``column_names``: <class 'tuple'>::

            (Key, Spider, Pnd, Run, Start, Finish, Err, Warn, Items,...)

        ``data``: <class 'tuple'>::

            (('299923/10/2', 'example.org', 0, 15, '2019/05/21 13:55',...),
             ('299923/10/1', 'example.org', 0, 10, '2019/05/20 18:37',...))

        ``zipped_columns``: <class 'zip'>::

            [('Key', ('299923/10/2', '299923/10/1')),
             ('Spider', ('example.org', 'example.org')),
             ('Pnd mins', (0, 0)),
             ('Run mins', (15, 10)),
             ('Start', ('2019/05/21 13:55', '2019/05/20 18:37')),
             ('Finish', ('2019/05/21 14:10', '2019/05/20 18:47')),
             ('Err', (0, 0)),
             ('Warn', (180, 179)),
             ('Items', (173, 174)),
             ('Pages', (177, 177)),
             ('Logs', (665, 651)),
             ('State', ('finished', 'finished')),
             ('Reason', ('finished', 'finished'))]

        ``cols_of_nums``: <class 'filter'>::

            [('Pnd mins', (0, 0)),
             ('Run mins', (15, 10)),
             ('Err', (0, 0)),
             ('Warn', (180, 179)),
             ('Items', (173, 174)),
             ('Pages', (177, 177)),
             ('Logs', (665, 651))]
        """
        data = tuple(data)
        if not data:
            return

        def title():
            params = (
                'content',
                'count',
                'jobkey',
                'project',
                'spider',
                'start',
                'tag',
            )
            args = dict((p, getattr(parsed_args, p, None)) for p in params)
            # if len(cols_of_nums) == 1:
            #     args['content'] = cols_of_nums[0][0]
            return ', '.join(f'{k}:{v}' for k, v in args.items() if v)

        def all_numbers(col):
            head, values = col
            try:
                return bool([float(v) for v in values])
            except (TypeError, ValueError):
                return False

        def get_x_values():
            index = 0
            if 'Key' in column_names:
                index = column_names.index('Key')
            elif '_key' in column_names:
                index = column_names.index('_key')
            return [row[index] for row in data]

        zipped_columns = zip(column_names, zip(*data))
        cols_of_nums = filter(all_numbers, zipped_columns)
        x = get_x_values()

        plotly.offline.plot({
            "data": [go.Bar(name=yaxis, x=x, y=y) for yaxis, y in cols_of_nums],
            "layout": go.Layout(title=title(), barmode='stack')
        }, auto_open=True)

    def emit_one(self, column_names, data, stdout, parsed_args):
        print(data)
