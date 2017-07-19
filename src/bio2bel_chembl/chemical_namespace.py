# -*- coding: utf-8 -*-

import logging
import os
import sqlite3
import sys

import click
import pandas as pd
from pybel.constants import NAMESPACE_DOMAIN_CHEMICAL
from pybel.constants import PYBEL_DATA_DIR
from pybel_tools.definition_utils import write_namespace

log = logging.getLogger(__name__)

CHEMBL_DATA_DIR = os.path.join(PYBEL_DATA_DIR, 'bio2bel', 'chembl')
if not os.path.exists(CHEMBL_DATA_DIR):
    os.makedirs(CHEMBL_DATA_DIR)

CHEMBL_SQLITE3_DB_DIR = os.path.join(CHEMBL_DATA_DIR, 'chembl_23_sqlite')
CHEMBL_DB = os.path.join(CHEMBL_SQLITE3_DB_DIR, "chembl_23.db")

SQLITE_SELECT_TEXT = """
select 
  chembl_id
from molecule_dictionary
"""


def get_data(db=None, sql=None):
    """Gets the source data.

    :param str db: path to sqlite database file
    :param str sql: SQL query command that will be executed
    :return: A data frame containing the original source data
    :rtype: pandas.DataFrame
    """
    db = CHEMBL_DB if db is None else db
    sql = SQLITE_SELECT_TEXT if sql is None else sql
    log.info(sql + ' __IN_ ' + CHEMBL_DB)
    db = sqlite3.connect(db)
    df = pd.read_sql_query(sql, db)
    return df


def get_chembl_molecule_names(df=None):
    """Processes the source data.

    :param pandas.DataFrame df: A data frame containing the original data source
    :return: Returns the set of current UniProt proteins Family names
    :rtype: set[str]
    """
    df = get_data() if df is None else df
    entries = set(df['chembl_id'].unique())
    return entries


def write_chemical_belns(file, df=None):
    """Writes the Entities as a BEL namespace file.

    :param file file: A writable file or file-like
    :param pandas.DataFrame df: A data frame containing the original data source
    """
    values = get_chembl_molecule_names(df=df)

    write_namespace(
        namespace_name="ChEMBL Molecules",
        namespace_keyword="CHEMBLA",
        namespace_domain=NAMESPACE_DOMAIN_CHEMICAL,
        namespace_species='9606',
        namespace_description="ChEMBL Identifiers for proteins",
        citation_url="http://chembl.blogspot.de/2017/05/chembl23-released.html",  # CHEMBL_MOLECULES_MAPPING,
        citation_name="ChEMBL molecules",
        author_name='Aram Grigoryan',
        author_contact="aram.grigoryan@scai.fraunhofer.de",
        author_copyright='Creative Commons by 4.0',
        values=values,
        functions="A",
        file=file
    )


@click.group(help='cli for bio2bel chembl')
def main():
    pass


@main.command()
@click.option('--output', type=click.File('w'), default=sys.stdout)
def write(output):
    write_chemical_belns(output)


if __name__ == '__main__':
    log.setLevel(20)
    logging.basicConfig(level=20)
    main()
