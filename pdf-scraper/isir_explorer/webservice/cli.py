from asyncio import events
from databases import Database
import click
import configparser
from .isir_requests import IsirRequests
from ..config import AppConfig

class IsirClient:

    def __init__(self, config):
        self.conf = config
        self.db = Database(self.conf['db.dsn'])

    async def run(self):
        await self.sync_isir_database()

    async def sync_isir_database(self):
        await self.db.connect()
        
        requests = IsirRequests(self.conf, self.db)
        await requests.start()

        await self.db.disconnect()
        if requests.exit_code:
            exit(requests.exit_code)

    def start_loop(self):
        loop = events.get_event_loop()
        loop.run_until_complete(self.run())


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
              required=True,
              show_default=True,
              default='app.cfg',
              type=click.File('r'),
              callback=validate_config_file)

def isirClient(config):

    app = IsirClient(config)
    app.start_loop()
