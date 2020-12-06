from .downloader import Downloader
from ..config import AppConfig
from asyncio import events
import click
import configparser


def validate_config_file(ctx, param, value):
    config = configparser.ConfigParser()
    config.optionxform = str    # maintain case sensitivity in keys
    str_content = value.read()
    config.read_string(str_content)

    if "db" not in config:
        raise click.BadParameter("V konfiguracnim souboru chybi sekce [db].")

    return AppConfig(config)


@click.command()
@click.option('-c', '--config',
              metavar='FILENAME',
              help='Cesta ke konfiguracnimu souboru.',
              show_default=True,
              default='app.cfg',
              type=click.File('r'),
              callback=validate_config_file)
@click.option('--debug',
              is_flag=True,
              default=False,
              help='Debug výpis do stdout.')
def isirDownloader(config, debug):
    if debug:
        config.set_opt("debug", True)
    dl = Downloader(config)
    loop = events.get_event_loop()
    loop.run_until_complete(dl.run())

