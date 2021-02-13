from .isir_scraper import IsirScraper
from ..config import AppConfig
import click
import configparser
from asyncio import events


def validate_config_file(ctx, param, value):
    config = configparser.ConfigParser()
    config.optionxform = str    # maintain case sensitivity in keys
    str_content = value.read()
    config.read_string(str_content)

    return AppConfig(config)


def validate_doctype(ctx, param, value):
    if value is None:
        return None

    parser = IsirScraper.getParserByName(value)

    if not parser:
        raise click.BadParameter(
            f"Zadaný typ dokumentu ({value}) není podporován.")

    return value


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
@click.option('-d', '--doctype',
              metavar='TYPE',
              help='Výběr typu dokumentu. Podporovane hodnoty: Prihlaska, PrehledovyList, ZpravaProOddluzeni, ZpravaPlneniOddluzeni, ZpravaSplneniOddluzeni. Pokud není zadáno, je použita automatická detekce dle obsahu vstupního PDF souboru.',
              callback=validate_doctype)
@click.option('-m', '--multidoc',
              is_flag=True,
              default=False,
              help='Aktivuje čtení více dokumentů z jednoho vstupního PDF. Výstupem je pole objektů s nalezenými dokumenty.')
@click.option('--save-text',
              is_flag=True,
              default=False,
              help='Do dočasného adresáře bude zapsána dekódovaná textová podoba PDF formuláře.')
@click.option('--debug',
              is_flag=True,
              default=False,
              help='Debug výpis do stdout.')
def isirScraper(pdf_file, output, config, doctype, multidoc, save_text, debug):
    config.set_opt("debug", debug)
    config.set_opt("doctype", doctype)
    config.set_opt("multidoc", multidoc)
    config.set_opt("sc.save_text", save_text)
    config.set_opt("sc._cli", True)
    config.set_opt("_out", output)
    parser = IsirScraper(pdf_file, config)
    loop = events.get_event_loop()
    loop.run_until_complete(parser.run())
