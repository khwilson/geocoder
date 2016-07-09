import json
import sys

import click
import requests

from geocoder import google
from geocoder.cache import Cache
from geocoder.compat import UnicodeCsvReader, UnicodeCsvWriter


class TooManyRetries(Exception):
    def __init__(self, msg, status_code):
        super(TooManyRetries, self).__init__(msg)
        self.status_code = status_code


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


@click.group()
def cli():
    pass


@cli.command('geocode')
@click.argument('credentials_file', type=click.Path(exists=True, dir_okay=False, file_okay=True))
@click.argument('input_file', type=click.Path(exists=True, dir_okay=False, file_okay=True))
@click.option('--output-file', '-o', type=click.Path(), default=None,
              help="Where to write the geocoding. Default is standard out")
@click.option('--cache', type=click.Path(), default=None,
              help='If passed, will cache the results of the geocoding (and will use a cache '
                   'previously created')
def geocode_command(credentials_file, input_file, output_file, cache):
    """Geocode the addresses at the passed location"""
    with open(credentials_file, 'r') as f:
        credentials = [line.strip() for line in f]

    key_iter = iter(credentials)
    key = next(key_iter)

    with UnicodeCsvReader(input_file) as input:
        num_rows = sum(1 for _ in input)

    with UnicodeCsvReader(input_file) as input, UnicodeCsvWriter(output_file) as output, \
            Cache(cache) as cache:
        with click.progressbar(input, label="Geocoding...", length=num_rows) as pb:
            for address, city, state, zip_code in pb:
                full_address = google.normalize_full_address(address, city, state, zip_code)
                value = cache.get(full_address)
    
                # If the value is not in the cache, query the API
                if not value:
                    while True:  # Used to loop over API keys
                        url = google.get_url(key, full_address)
                        try:
                            value = get_with_retry(url)
                        except TooManyRetries:
                            click.echo("Too many retries while getting {}".format(url))
                            click.echo("Exiting....")
                            sys.exit(1)
                        if value['status'] in ('OVER_QUERY_LIMIT', 'REQUEST_DENIED'):
                            if value['status'] == 'REQUEST_DENIED':
                                click.echo("Denied request while using key {}".format(key))
                            try:
                                key = next(key_iter)
                            except StopIteration:
                                click.echo("Ran out of keys!")
                                click.echo("Exiting....")
                                sys.exit(1)
                            continue
                        cache[full_address] = value
                        break
                output.writerow([full_address, json.dumps(value)])


if __name__ == '__main__':
    cli()
