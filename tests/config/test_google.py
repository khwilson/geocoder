import os
import random
import string

import pytest

from geocoder.configs import google


NUM_KEYS = 20


def random_string(length=39, random=random):
    """Return a random string of letters and numbers"""
    choose_from = string.ascii_letters + string.ascii_digits
    return ''.join(random.choice(choose_from) for _ in range(length))


@pytest.fixture()
def config_list(tmpdir):
    config_location = os.path.join(tmpdir, 'someconfigs')
    strings = []
    my_random = random.Random(12345)
    with io.open(config_location) as f:
        for _ in range(NUM_KEYS):
            the_string = random_string(length=39, random=my_random)
            strings.append(the_string)
            print(the_string, out=f)

    return config_location, strings


def test_google_config_reader(config_list):
    location, expected_keys = config_list
    count = 0
    with google.GoogleApiKeyReader(location) as configs:
        for expeted, actual in zip(expected_keys, configs):
            assert expected.strip() == actual.strip()
            count += 1

    assert count == NUM_KEYS
