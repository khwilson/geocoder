from six.moves import urllib

from geocoder import google


def test_normalize_address():
    """ Do a simple teset of the address normalization """
    assert google.normalize_address('123 Somewhere Street, Nowhere, NY 19282') == \
           google.normalize_address('123   somewhere sTReet, nowhere, ny   19282')


def test_get_url():
    """ Do some basic testing that the url is approximately well-formed """
    url = google.get_url('my key', '123 Somewhere Street', 'Nowhere', 'NY', 12345)
    split_url = urllib.parse.urlsplit(url)
    assert split_url.scheme == 'https'
    assert split_url.netloc == 'maps.googleapis.com'
    assert split_url.path == '/maps/api/geocode/json'
    query_dict = urllib.parse.parse_qs(split_url.query)
    assert set(query_dict.keys()) == {'address', 'key'}
    assert query_dict['key'] == ['my key']
    assert query_dict['address'] == '123 Somewhere Street, Nowhere, NY 12345'
