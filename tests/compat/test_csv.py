from __future__ import unicode_literals

import os

from geocoder.compat import UnicodeCsvReader, UnicodeCsvWriter


def test_regular(tempdir):
    """Make sure compatible reader works with regular csvs"""
    filename = os.path.join(tempdir, 'test.csv')
    with UnicodeCsvWriter(filename) as writer:
        writer.writerow(['a', 'b', 'c'])
        writer.writerow(['d', 'e', 'f'])

    with UnicodeCsvReader(filename) as reader:
        both_rows = reader.readrows()
        assert len(both_rows) == 2
        assert both_rows[0] == ['a', 'b', 'c']
        assert both_rows[1] == ['d', 'e', 'f']


def test_gzipped(tempdir):
    """Make sure compatible reader works with gzipped csvs"""
    filename = os.path.join(tempdir, 'test.csv.gz')
    with UnicodeCsvWriter(filename) as writer:
        writer.writerow(['a', 'b', 'c'])
        writer.writerow(['d', 'e', 'f'])

    with UnicodeCsvReader(filename) as reader:
        both_rows = reader.readrows()
        assert len(both_rows) == 2
        assert both_rows[0] == ['a', 'b', 'c']
        assert both_rows[1] == ['d', 'e', 'f']
