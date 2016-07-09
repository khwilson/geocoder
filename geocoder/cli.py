import json
import sys

import click

from geocoder import google
from geocoder.cache import Cache
from geocoder.compat import UnicodeCsvReader, UnicodeCsvWriter


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

    manager = google.RequestManger(credentials)

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
                    try:
                        value = manager.resolve(full_address)
                    except google.TooManyRetries:
                        click.echo("Too many retries while getting {}".format(url))
                        click.echo("Exiting....")
                        sys.exit(1)
                    except google.OutOfKeys:
                        click.echo("Ran out of keys!")
                        click.echo("Exiting....")
                        sys.exit(1)
                    cache[full_address] = value
                output.writerow([full_address, json.dumps(value)])


if __name__ == '__main__':
    cli()
