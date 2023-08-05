import logging
from typing import TextIO

import click

from .core import Observer, Converter, MultiConverter, FileManager


@click.group()
def main() -> None:
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)


@main.command()
@click.option('-o', '--output-file', type=click.File('w'))
@click.argument('markdown-file', required=False, type=click.File())
def convert(output_file: TextIO, markdown_file: TextIO) -> None:
    if output_file is None:
        output_file = click.get_text_stream('stdout')
    if markdown_file is None:
        markdown_file = click.get_text_stream('stdin')
    Converter().convert(markdown_file, output_file)


@main.command()
@click.argument('md-root', type=click.Path(exists=True))
@click.argument('html-root', type=click.Path())
def convert_all(md_root: str, html_root: str) -> None:
    MultiConverter(FileManager(md_root, html_root)).convert_all()


@main.command()
@click.argument('md-root', type=click.Path(exists=True))
@click.argument('html-root', type=click.Path())
def watch(md_root: str, html_root: str) -> None:
    Observer(md_root, html_root).watch()


if __name__ == '__main__':
    main()
