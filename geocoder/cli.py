import click


@click.group()
def cli():
    pass


@cli.command('geocode')
def geocode_command():
    pass


if __name__ == '__main__':
    cli()
