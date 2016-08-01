import enum
import re

import requests
from six.moves import urllib


# The URL to call the geocoding API
GOOGLE_GEOCODE_URL = 'https://maps.googleapis.com/maps/api/geocode/'


class RETURN_TYPE(enum.Enum):
    """ The available return types from the geocoding API """
    JSON = 'json'
    XML = 'xml'


def normalize_address(address):
    """Do some basic normalization of the passed address so we don't have
    to make so many calls to the geocoding API.

    :param str address: The address (part) to normalize
    :return: The basic normalized version of the address
    :rtype: str
    """
    address = address.lower().strip()
    address = re.sub(r'\s+', ' ', address)
    return address


def normalize_full_address(address, city, state, zip_code):
    address = normalize_address(address)
    city = normalize_address(city)
    state = normalize_address(state)
    zip_code = normalize_address(zip_code)
    full_address = '{address}, {city}, {state} {zip_code}'.format(
        address=address, city=city, state=state, zip_code=zip_code)
    return full_address


def get_url(key, full_address, return_type=RETURN_TYPE.JSON):
    """Return a URL to geocode the passed address.

    :param str key: Your api key
    :param str full_address: The street address you want to geocode
    :param str city: The city of the address you want to geocode
    :param str state: The state (two characters like KY) of the address
        you want to geocode
    :param str|int zip_code: The zip code of the address you want to geocode
    :param RETURN_TYPE return_type: What return type would you like?
    :return: The url for geocoding
    :rtype: str
    """
    url = urllib.parse.urljoin(GOOGLE_GEOCODE_URL, return_type.value)
    url += '?' + urllib.parse.urlencode({'address': full_address, 'key': key})
    return url


class TooManyRetries(Exception):
    def __init__(self, msg, status_code):
        super(TooManyRetries, self).__init__(msg)
        self.status_code = status_code


class OutOfKeys(Exception):
    pass


def get_with_retry(url, start_wait=1, wait_exponent=2, num_tries=3):
    """Get a URL but perform exponential backoff if a non good status code is returned
    Note that we assume the content is JSON.

    :param str url: The URL to retreive
    :param float start_wait: The first waiting time on an unsuccessful get
    :param float wait_exponent: The exponent between waiting times
    :param int num_tries: The number of times to retry before giving up
    :raises TooManyRetries: If we run out of retries
    :return: The response content (assumed JSON) as a dict
    :rtype: dict
    """
    wait = start_wait
    for try_num in range(num_tries):
        response = requests.get(url)
        if response.ok:
            return response.json()
        wait *= wait_exponent
    raise TooManyRetries("Too many retries for url {}".format(url), response.status_code)


class RequestManger(object):
    """A little wrapper that manages keys and resolving addresses"""

    def __init__(self, keys):
        """
        :param list[str] keys: The Geocoding API keys you wish to use
        """
        self.keys = keys
        self.key_iter = iter(keys)
        self.key = next(self.key_iter)

    def resolve(self, address):
        """Resolve an address with the Google API

        :return: The JSON that is returned by the API
        :rtype: dict
        :raises OutOfKeys: If we have run out API keys for the day
        :raises TooManyRetries: If we have retried the call too many times
        """
        while True:  # Used to iterate over keys
            url = get_url(self.key, address)
            value = get_with_retry(url)
            if value['status'] in ('OVER_QUERY_LIMIT', 'REQUEST_DENIED'):
                try:
                    self.key = next(self.key_iter)
                except StopIteration:
                    raise OutOfKeys
                continue
            return value
