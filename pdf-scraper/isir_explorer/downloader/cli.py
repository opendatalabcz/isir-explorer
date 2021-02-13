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
@click.option('--limit',
              default=False,
              type=click.INT,
              help='Omezit počet dokumentů ke stažení.')
@click.option('--start',
              default=False,
              type=click.INT,
              help='ID události v rejstříku, od které zahájit stahování.')
@click.option('--debug',
              is_flag=True,
              default=False,
              help='Debug výpis do stdout.')
def isirDownloader(config, limit, start, debug):
    if debug:
        config.set_opt("debug", True)

    if start and start > 0:
        config.set_opt("dl.start", start)

    if limit and limit > 0:
        # Kontrola, ze pocet soubezne stahovanych nebude vetsi nez limit pro stahovani
        if config["dl.concurrency"] > limit:
            config.set_opt("dl.concurrency", limit)
        config.set_opt("dl.limit", limit)

    dl = Downloader(config)
    loop = events.get_event_loop()
    try:
        loop.run_until_complete(dl.run())
    except KeyboardInterrupt:
        dl.forceStop = True
        loop.run_forever()
        loop.close()
