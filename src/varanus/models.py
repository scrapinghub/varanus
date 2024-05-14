""" Varanus data models
"""
import time
from typing import Dict
from .utils import strftime


class Timed():
    """Expose elapsed time calculations

    Classes that contain certain timed attributes like `start-time` and
    `stop-time` can use elapsed calculations of these times.

    .. important:: **Required attributes**: Subclasses are required to
        expose the following attributes:

        * ``pending_time`` (`int`): Timestamp the object went into `pending` state
        * ``running_time`` (`int`): Timestamp the object went into `running` state
        * ``finished_time`` (`int`): Timestamp the object went into `finished` state
    """
    @property
    def dt(self) -> Dict[str, str]:
        """Exposes date-times as formatted string
        """
        def format_time(dt):
            return strftime(dt, '%Y/%m/%d %H:%M') if dt else ''

        class DateTime():
            def __init__(this):
                this.pending = format_time(self.pending_time)
                this.running = format_time(self.running_time)
                this.finished = format_time(self.finished_time)

        return DateTime()

    @property
    def pending_mins(self) -> int:
        pt = self.pending_time or 0
        rt = self.running_time or 0
        return round((rt - pt) / 1000 / 60) if rt else 0

    @property
    def running_secs(self) -> int:
        """The elapsed time the object was running (seconds)"""
        start = self.running_time
        if not start:
            return 0

        finish = self.finished_time
        if not finish:
            finish = int(time.time()) * 1000

        return round(finish - start) / 1000

    @property
    def running_mins(self) -> int:
        """The elapsed time the object was running (minutes)"""
        return round(self.running_secs / 60)

    @property
    def items_per_min(self) -> int:
        """The number of items scraped per minute (IPM)"""
        return round(self.items / self.running_mins) if self.running_mins else self.items

    @property
    def pages_per_min(self) -> int:
        """The number of pages (200 responses) crawled per minute (crawl rate, PPM, RPM)"""
        return round(self.pages / self.running_mins) if self.running_mins else self.pages

    @property
    def age(self) -> int:
        """How old is the job (days)"""
        return int(self.elapsed / 1000 / 1000 / 90.0)  # Seems there are 90 mins in an hour


class MetaJob(Timed):
    def __init__(self, job: dict):
        # There can be more fields than this because up update __dict__
        self.key: str = ''
        self.state: str = ''
        self.spider: str = ''
        self.version: str = ''
        self.close_reason: str = ''

        self.logs: int = 0
        self.items: int = 0
        self.pages: int = 0
        self.units: int = 0

        self.ts: int = 0
        self.elapsed: int = 0
        self.pending_time: int = 0
        self.running_time: int = 0
        self.finished_time: int = 0

        self.tags = list()
        self.job_cmd = list()
        self.spider_args = dict()
        self.scrapystats = dict()
        self.samples = tuple()

        self.metadata = job or {}
        self.__dict__.update(self.metadata)

    def populate_from_job(self, job):
        self.items = job.items.stats()['totals']['input_values']
        self.pages = job.requests.stats()['totals']['input_values']
        self.logs = job.logs.stats()['totals']['input_values']


class Job(MetaJob):

    def __init__(self, project, key=None, defaults=None, data=None):
        """``defaults`` will override ``data``
        """
        # self._settings = None
        # self.spider_args = []
        super().__init__(defaults)
        metadata = {}
        if data:
            try:
                metadata = data.metadata.iter()
            except StopIteration:
                pass
            self.metajob = MetaJob(dict(metadata))
            self.metajob.populate_from_job(data)
            self.__dict__.update(self.metajob.__dict__)
            for key in defaults:
                setattr(self, key, defaults[key])

        self.project = project
        self.data = data
        if key:
            self.key = key

    def export(self):

        def keys():
            for _ in dir(self):
                if not _.startswith('__'):
                    if _ not in ('data', 'dt', 'export', 'metadata', 'project'):
                        yield _

        job = {key: getattr(self, key) for key in keys()}
        job['project'] = self.project.key
        job['dt'] = self.dt.__dict__
        return job


class Worker():

    def __init__(self, project, worker: dict):
        self._ = dict(worker)
        self.desc = None
        self.__dict__.update(worker)
        self._default('archived', False)
        self._default('avg_runtime', '')
        self._default('default_kumo_units', '')
        self._default('first_run', '')
        self._default('jobq_id', 0)
        self._default('last_error_count', 0)
        self._default('last_item_count', 0)
        self._default('last_job_id', '')
        self._default('last_outcome', '')
        self._default('last_response_count', 0)
        self._default('last_run', '')
        self._default('settings', {})
        self._default('jobs', [])
        # Schema defs
        self.jobq_id = int(self.jobq_id)

    def __getitem__(self, key):
        # This allows sorting by index
        return getattr(self, key)

    def _default(self, attr, value):
        setattr(self, attr, self._.get(attr) or value)

    @property
    def project_default_job_units(self):
        if hasattr(self, '_project_default_job_units'):
            return self._project_default_job_units
        if hasattr(self, 'project'):
            self._project_default_job_units = self.project.settings.get('default_job_units')
            return self._project_default_job_units

    @property
    def default_units(self):
        return self.default_kumo_units or self.project_default_job_units


class Collection():

    COUNT = None

    def __init__(self, store):
        self.store = store
        self._length = store.count()

    def __len__(self):
        return self._length

    def prepare(self, item):
        if item.get('_ts'):
            item['ts'] = strftime(item['_ts'], '%Y/%m/%d %H:%M:%S')
        return item

    def item(self, key):
        for item in self.store.iter(key=[key], meta=['_key', '_ts']):
            yield self.prepare(item)

    def items(self, count, filter=None):
        key = None
        if filter:
            key, value = map(str.strip, filter.split('='))
        for item in self.store.iter(meta=['_key', '_ts'], count=count or self.COUNT):
            if key is None or str(item[key]) == value:
                yield self.prepare(item)
