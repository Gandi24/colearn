# -*- coding: utf-8 -*-
from formats import FormatBank, default_bank


def discover_str(bank=None, **meta):
    if bank is None:
        bank = default_bank
    bank.register('str', lambda x: x, lambda x: x, **meta)


def setup_format_str(formats=None):
    discover_str(formats, content_type='application/json')
