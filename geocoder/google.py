import enum
import re

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
    address = google.normalize_address(address)
    city = google.normalize_city(city)
    state = google.normalize_state(state)
    zip_code = google.normalize_zip_code(zip_code)
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
