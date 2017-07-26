# -*- coding: utf-8 -*-

import sys

import click
from pybel_tools.resources import get_today_arty_namespace, deploy_namespace

from .chemical_namespace import write_chemical_belns


@click.group(help='cli for bio2bel chembl')
def main():
    pass


@main.command()
@click.option('--output', type=click.File('w'), default=sys.stdout)
def write(output):
    write_chemical_belns(output)


@main.command()
def deploy():
    """deploys chemical namespace to artifactory"""
    f_name = get_today_arty_namespace("chembla")

    with open(f_name, 'w') as file:
        write_chemical_belns(file)

    deploy_namespace(f_name, 'chembla')


if __name__ == '__main__':
    main()
