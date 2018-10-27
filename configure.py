#!/usr/bin/env python
import codecs
import os

import click
from jinja2 import Environment, FileSystemLoader


@click.command()
@click.option('--variant', type=click.Choice(['gpu', 'cpu']))
def main(variant):
    source_root = os.path.split(os.path.abspath(__file__))[0]
    env = Environment(loader=FileSystemLoader(source_root))
    template = env.get_template('Dockerfile.template')
    is_gpu = variant == 'gpu'
    docker_file = os.path.join(source_root, 'Dockerfile')

    with codecs.open(docker_file, 'wb', 'utf-8') as f:
        f.write(template.render(gpu=is_gpu) + '\n')


if __name__ == '__main__':
    main()
