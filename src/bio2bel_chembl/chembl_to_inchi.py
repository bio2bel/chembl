# -*- coding: utf-8 -*-
"""Download ftp://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/latest/chembl_23_chemreps.txt.gz
Unpack chembl_23_chemreps.txt into CHEMBL_DATA_DIR"""
import os
import sqlite3
import logging
import pandas as pd

log = logging.getLogger(__name__)

from pybel.constants import PYBEL_DATA_DIR
from pybel_tools.definition_utils import write_namespace
from pybel_tools.document_utils import write_boilerplate
from pybel.constants import IS_A
from pybel.utils import ensure_quotes
from pybel_tools.resources import INCHI_PATTERN

CHEMBL_DATA_DIR = os.path.join(PYBEL_DATA_DIR, 'bio2bel', 'chembl')
if not os.path.exists(CHEMBL_DATA_DIR):
    os.makedirs(CHEMBL_DATA_DIR)

CHEMBL_CHEMREPS_FILE = os.path.join(CHEMBL_DATA_DIR, 'chembl_23_chemreps.txt')

def get_data():
    """Gets the source data.

    :param str db: path to sqlite database file
    :param str sql: SQL query command that will be executed
    :return: A data frame containing the original source data
    :rtype: pandas.DataFrame
    """
    df = pd.read_csv(
        CHEMBL_CHEMREPS_FILE,
        sep='\t',
        skiprows=1,
        names=['chembl_id',	'canonical_smiles',	'standard_inchi',	'standard_inchi_key']
    )
    return df

def write_chembl_inchi_belscript(file, df=None):
    """Writes the ChEMBL ID to inchi equivalence a BEL script

    :param file file: A writable file or file-like
    :param pandas.DataFrame df: A data frame containging the original data source
    """

    df = get_data() if df is None else df

    write_boilerplate(
        document_name='ChEMBL ID to inchi equivalence',
        authors='Aram Grigoryan',
        contact='aram.grigoryan@scai.fraunhofer.de',
        licenses='Creative Commons by 4.0',
        copyright='Copyright (c) 2017 Charles Tapley Hoyt. All Rights Reserved.',
        description="""This BEL document represents ChEMBL ID to inchi strings equivalence""",
        namespace_dict={
            'CHEMBLA': 'https://arty.scai.fraunhofer.de/artifactory/bel/namespace/chembla/chembla-20170719.belns',
            'INCHI': INCHI_PATTERN,
        },
        namespace_patterns={},
        annotations_dict={},
        annotations_patterns={},
        file=file
    )

    print('SET Citation = {{"URL","{}"}}'.format("http://chembl.blogspot.de/2017/05/chembl23-released.html"), file=file)
    print('SET Evidence = "ChEMBL to INCHI mapping"', file=file)

    for _,chembl_id, standard_inchi in df[['chembl_id', 'standard_inchi']].itertuples():
        chembl_clean = ensure_quotes(str(chembl_id).strip())
        inchi_clean = ensure_quotes(str(standard_inchi).strip())

        if chembl_clean == 'nan' or inchi_clean == 'nan':
            continue

        print('a(CHEMBLA:{}) eq a(INCHI:{})'.format(chembl_clean, inchi_clean), file=file)

if __name__ == '__main__':
    log.setLevel(20)
    logging.basicConfig(level=20)
    dff = get_data()
    with open(os.path.join(CHEMBL_DATA_DIR, 'chembl_to_inchi.bel'), 'w') as f:
        write_chembl_inchi_belscript(f, dff)
    #log.info(dff.head())
