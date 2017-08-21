# -*- coding: utf-8 -*-
"""
Download file ftp://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/latest/chembl_23_sqlite.tar.gz
Unzip chembl_23.db file into $HOME/.pybel/data/bio2bel/chembl/chembl_23_sqlite/
"""
import logging
import os
import sqlite3

import pandas as pd
from pybel.constants import PYBEL_DATA_DIR
from pybel.utils import ensure_quotes
from pybel_tools.document_utils import write_boilerplate

log = logging.getLogger(__name__)

CHEMBL_DATA_DIR = os.path.join(PYBEL_DATA_DIR, 'bio2bel', 'chembl')
if not os.path.exists(CHEMBL_DATA_DIR):
    os.makedirs(CHEMBL_DATA_DIR)

CHEMBL_SQLITE3_DB_DIR = os.path.join(CHEMBL_DATA_DIR, 'chembl_23_sqlite')
CHEMBL_DB = os.path.join(CHEMBL_SQLITE3_DB_DIR, "chembl_23.db")


def sql_query(standard_type='IC50', standard_value=10000):
    SQLITE_SELECT_TEXT = """
select target_dictionary.chembl_id as chembl_target_p , chembl_molecule_id
from target_dictionary join
(select chembl_molecule_id, tid
from assays join
(select molecule_dictionary.chembl_id as chembl_molecule_id, molregno, activity_id, assay_id
from molecule_dictionary join ( select molregno, activity_id, assay_id
								from activities
								where standard_type = '{}' and standard_value <= {})
						 using (molregno) ) using (assay_id)) using (tid);
""".format(standard_type, standard_value)
    return SQLITE_SELECT_TEXT


def get_data(db=None, sql=None, standard_type='IC50', standard_value=10000):
    """Gets the source data.

    :param str db: path to sqlite database file
    :param str sql: SQL query command that will be executed
    :return: A data frame containing the original source data
    :rtype: pandas.DataFrame
    """
    db = CHEMBL_DB if db is None else db
    sql = sql_query(standard_type=standard_type, standard_value=standard_value) if sql is None else sql

    db = sqlite3.connect(db)
    df = pd.read_sql_query(sql, db)
    return df


def write_chemical_inhibition_file(file, df=None, standard_type='IC50', standard_value=10000):
    """Writes the ChEMBL ID to inchi equivalence a BEL script

    :param file file: A writable file or file-like
    :param pandas.DataFrame df: A data frame containging the original data source
    """

    df = get_data(standard_type=standard_type, standard_value=standard_value) if df is None else df

    write_boilerplate(
        document_name='ChEMBL Chemical Inhibition Activity BEL script',
        authors='Aram Grigoryan',
        contact='aram.grigoryan@scai.fraunhofer.de',
        licenses='Creative Commons by 4.0',
        copyright='Copyright (c) 2017 Aram Grigoryan. All Rights Reserved.',
        description="""This BEL document represents chemical inhibition information, with standard_type = '{}', standard_value = {}""".format(
            standard_type, standard_value),
        namespace_dict={
            'CHEMBLA': 'https://arty.scai.fraunhofer.de/artifactory/bel/namespace/chembla/chembla-20170719.belns',
            'CHEMBLP': 'n/a',
        },
        namespace_patterns={},
        annotations_dict={},
        annotations_patterns={},
        file=file
    )

    print('SET Citation = {{"URL","{}"}}'.format("http://chembl.blogspot.de/2017/05/chembl23-released.html"), file=file)
    print('SET Evidence = "ChEMBL to INCHI mapping"', file=file)

    for _, molecule_id, prot_id in df[['chembl_molecule_id', 'chembl_target_p']].itertuples():
        molecule_clean = ensure_quotes(str(molecule_id).strip())
        prot_clean = ensure_quotes(str(prot_id).strip())

        if molecule_clean == 'nan' or prot_clean == 'nan':
            continue

        print('a(CHEMBLA:{}) = | act(p(CHEMBLP:{}))'.format(molecule_clean, prot_clean), file=file)


if __name__ == '__main__':
    log.setLevel(20)
    logging.basicConfig(level=20)

    dff = get_data(standard_type='IC50', standard_value=10000)
    # log.info(dff.head())
    with open(os.path.join(CHEMBL_DATA_DIR, 'chemical_inhibition.bel'), 'w') as f:
        write_chemical_inhibition_file(f, dff, standard_type='IC50', standard_value=10000)
