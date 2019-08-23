"""Scrapinghub spiders access
"""
from .workers import Workers as _Workers  # noqa


class Workers(_Workers):
    paths = ('spiders',)
