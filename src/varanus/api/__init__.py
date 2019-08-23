"""Python interface (external)
"""
import varanus.lib
import varanus.session

__all__ = ['Jobs']


def Jobs(**kwargs):
    for job in varanus.lib.Jobs(varanus.session.Session(), **kwargs):
        yield job.export()
