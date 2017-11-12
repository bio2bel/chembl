# -*- coding: utf-8 -*-

import sys

import click

from pybel.resources.arty import get_today_arty_namespace
from pybel.resources.deploy import deploy_namespace
from .chemical_namespace import write_chemical_belns


@click.group()
def main():
    """ChEMBL to BEL"""


@main.command()
@click.option('--output', type=click.File('w'), default=sys.stdout)
def write(output):
    """Write chemical namespace"""
    write_chemical_belns(output)


@main.command()
def deploy():
    """Deploy chemical namespace to Artifactory"""
    f_name = get_today_arty_namespace("chembla")

    with open(f_name, 'w') as file:
        write_chemical_belns(file)

    deploy_namespace(f_name, 'chembla')


if __name__ == '__main__':
    main()
