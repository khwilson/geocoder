import os

from geocoder.cache import Cache


def test_no_cache():
    """ Test the cache when we don't provide a filename """
    with Cache(None) as cache:
        assert cache == {}


def test_write_and_read_cache(tempdir):
    """ Test the cache when we *do* provide a filename """
    cache_file = os.path.join(tempdir, 'temp_cache.csv.gz')
    with Cache(cache_file) as cache:
        assert cache == {}
        cache['a'] = {'foo': 1, 'bar': 2}
        cache['b'] = {'boo': 3, 'baz': 4}

    with Cache(cache_file) as cache:
        assert cache == {
            'a': {'foo': 1, 'bar': 2},
            'b': {'boo': 3, 'baz': 4}
        }

