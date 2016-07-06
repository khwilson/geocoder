from __future__ import print_function

import io
import os
import random

import pytest

from geocoder.config import google


NUM_KEYS = 20


def random_string(length=39, random=random):
    """Return a random string of letters and numbers"""
    choose_from = u'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    return ''.join(random.choice(choose_from) for _ in range(length))


@pytest.fixture()
def config_list(tempdir):
    config_location = os.path.join(tempdir, 'someconfigs')
    strings = []
    my_random = random.Random(12345)
    with io.open(config_location, 'w') as f:
        for _ in range(NUM_KEYS):
            the_string = random_string(length=39, random=my_random)
            strings.append(the_string)
            print(the_string, file=f)

    return config_location, strings


def test_google_config_reader(config_list):
    location, expected_keys = config_list
    count = 0
    with google.GoogleApiKeyReader(location) as configs:
        for expected, actual in zip(expected_keys, iter(configs)):
            assert expected.strip() == actual.strip()
            count += 1

    assert count == NUM_KEYS
