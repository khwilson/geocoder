from collections import Mapping

import json
import os

from geocoder.compat import UnicodeCsvReader, UnicodeCsvWriter


class AlwaysEmptyDict(Mapping):
    def __getitem__(self, key):
        raise KeyError

    def __setitem__(self, key, value):
        return

    def __iter__(self):
        return iter([])

    def __len__(self):
        return 0


def read_cache(cache_file):
    """Read a cache in from disk

    :param str|None cache_file: The link to the cache file. If it ends in gz, assume it's
        a gzipped CSV. Else, assume it's a regular CSV. If None, return {}
    :return: The cache, having keys the *normalized* addresses and values the dictionary
        returned from the Google API
    :rtype: dict[str, dict]
    """
    if not cache_file:
        return AlwaysEmptyDict()

    with UnicodeCsvReader(cache_file) as reader:
        return {key: json.loads(value) for key, value in reader}


def write_cache(cache, cache_file):
    """Write a cache in from disk

    :param dict[str, dict] cache: The cache to write to disk.
    :param str|None cache_file: The cache file location. If it ends in gz, assume it's
        a gzipped CSV. Else, assume it's a regular CSV. If None, noop.
    :return: The cache, having keys the *normalized* addresses and values the dictionary
        returned from the Google API
    :rtype: dict[str, dict]
    """
    if not cache_file:
        return

    with UnicodeCsvWriter(cache_file) as writer:
        for key, value in cache.items():
            writer.writerow([key, json.dumps(value)])


class Cache(object):
    def __init__(self, cache_file):
        self.cache_file = cache_file

    def __enter__(self):
        if not (self.cache_file and os.path.exists(self.cache_file)):
            self.cache = {}
        else:
            self.cache = read_cache(self.cache_file)
        return self.cache

    def __exit__(self, *args):
        write_cache(self.cache, self.cache_file)


