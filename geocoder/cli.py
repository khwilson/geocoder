import json
import sys

import click

from geocoder import google
from geocoder.cache import Cache, read_cache
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
                        click.echo("Too many retries while getting {}".format(full_address))
                        click.echo("Exiting....")
                        sys.exit(1)
                    except google.OutOfKeys:
                        click.echo("Ran out of keys!")
                        click.echo("Exiting....")
                        sys.exit(1)
                    cache[full_address] = value
                output.writerow([full_address, json.dumps(value)])


def get_not_ok(cache, exclude_keys=None):
    exclude_keys = exclude_keys or {}
    return {key: value for key, value in cache.items()
            if key not in exclude_keys and value['status'] != 'OK'}


def get_multiple_results(cache, exclude_keys=None):
    exclude_keys = exclude_keys or {}
    return {key: value for key, value in cache.items()
            if key not in exclude_keys and len(value['results']) > 1}


def get_no_street(cache, exclude_keys=None):
    exclude_keys = exclude_keys or {}
    def parse_result(result):
        if len(result) != 1:
            return False
        result = result['results'][0]
        types = {x['types'] for x in results['address_components']}
        return not ({'street_number', 'route'} <= types)

    return {key: value for key, value in cache.items()
            if key not in exclude_keys and parse_result(value)}


@cli.command('fixup')
@click.argument('credentials_file', type=click.Path(exists=True, dir_okay=False, file_okay=True))
@click.argument('input_file', type=click.Path(exists=True, dir_okay=False, file_okay=True))
@click.option('--output-file', '-o', type=click.Path(), default=None,
              help="Where to write the geocoding. Default is standard out")
def fixup_command(credentials_file, input_file, output_file):
    """Fixup geocodings coming from the `geocode` command that resulted in bad geocodes.
    Most likely because of a badly formatted or spelled address.

    INPUT_FILE should be in the format that came out of the `geocode` command. The output-file
    will be in a three column format: INPUT_FILE's key, the edited address, and then the *new*
    json dump from the geocoding API. The default output is stdout.
    """
    with open(credentials_file, 'r') as f:
        credentials = [line.strip() for line in f]

    manager = google.RequestManger(credentials)

    input_geocodes = read_cache(input_file)

    marker = '# All ignored after here'
    exclude_keys = set()  # Keep track of rows already fixed
    with UnicodeCsvWriter(output_file) as output:
        for function, description in ((get_not_ok, 'without OK status'),
                                      (get_multiple_results, 'with multiple results'),
                                      (get_no_street, 'without a street')):
            bad_geocodes = function(input_geocodes, exclude_keys=exclude_keys)
            if click.confirm("There are {} geocodes {}. Edit?".format(len(bad_geocodes), description)):
                for key, value in bad_geocodes.items():
                    while True:  # For multiple edits
                        edited = click.edit(key + '\n\n' + marker + '\n\n' +
                                            json.dumps(value, indent=2))
                        edited = edited.rsplit(marker, 1)[0].strip()
                        edited = google.normalize_address(edited)
                        value = manager.resolve(edited)
                        click.echo(json.dumps(value, indent=2))
                        if click.confirm("Good enough?"):
                            output.writerow([key, edited, json.dumps(value)])
                            break
            exclude_keys.update(bad_geocodes.keys())

if __name__ == '__main__':
    cli()
