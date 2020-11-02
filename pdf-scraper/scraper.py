from isir_scraper import IsirScraper
from config import AppConfig
import click
import configparser


def validate_config_file(ctx, param, value):
    config = configparser.ConfigParser()
    config.optionxform = str    # maintain case sensitivity in keys
    str_content = value.read()
    config.read_string(str_content)

    return AppConfig(config)

@click.command()
@click.argument('PDF_FILE',
                type=click.STRING,
                required=True)
@click.option('--debug',
              is_flag=True,
              default=False,
              help='Aktivuje debug vypis do stdout.')
@click.option('-c', '--config',
              metavar='FILENAME',
              help='Cesta ke konfiguracnimu souboru aplikace.',
              required=True,
              show_default=True,
              default='app.cfg',
              type=click.File('r'),
              callback=validate_config_file)
def startParser(pdf_file, config, debug):
    parser = IsirScraper(pdf_file, config)
    parser.run()

if __name__ == '__main__':
    startParser()
