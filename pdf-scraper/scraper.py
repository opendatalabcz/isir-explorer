from isir_scraper import IsirScraper
import click


@click.command()
@click.argument('FILE',
                type=click.STRING,
                required=True)
@click.option('--debug',
              is_flag=True,
              default=False,
              help='If set, will output log to stdout.')
def startParser(file, debug):
    parser = IsirScraper(file)
    parser.run()

if __name__ == '__main__':
    startParser()
