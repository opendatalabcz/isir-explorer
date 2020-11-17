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
@click.option('-o', '--output',
              default='-',
              type=click.File('w'),
              show_default=True,
              help='Výstupní soubor nebo - pro stdout.')
@click.option('-c', '--config',
              metavar='FILENAME',
              help='Cesta ke konfiguracnimu souboru.',
              show_default=True,
              default='app.cfg',
              type=click.File('r'),
              callback=validate_config_file)
@click.option('-m', '--multidoc',
              is_flag=True,
              default=False,
              help='Aktivuje čtení více dokumentů z jednoho vstupního PDF. Výstupem je pole objektů s nalezenými dokumenty.')
@click.option('--debug',
              is_flag=True,
              default=False,
              help='Debug výpis do stdout.')
def startParser(pdf_file, output, config, multidoc, debug):
    config.set_opt("debug", debug)
    config.set_opt("multidoc", multidoc)
    config.set_opt("_out", output)
    parser = IsirScraper(pdf_file, config)
    parser.run()

if __name__ == '__main__':
    startParser()
