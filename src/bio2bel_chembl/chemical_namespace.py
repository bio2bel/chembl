# -*- coding: utf-8 -*-

import sqlite3
import os
import pandas as pd
from pybel.constants import PYBEL_DATA_DIR



CHEMBL_DATA_DIR = os.path.join(PYBEL_DATA_DIR, 'bio2bel', 'chembl')
if not os.path.exists(CHEMBL_DATA_DIR):
    os.makedirs(CHEMBL_DATA_DIR)

CHEMBL_SQLITE3_DB_DIR = os.path.join(CHEMBL_DATA_DIR, 'chembl_23_sqlite')
CHEMBL_DB = CHEMBL_SQLITE3_DB_DIR + "/chembl_23.db"

SQLITE_SELECT_TEXT = "select * from molecule_dictionary ;"
test_query = 'select molecule_dictionary.chembl_id, molecule_dictionary.chebi_par_id, molecule_synonyms.molsyn_id, molecule_synonyms.res_stem_id from molecule_dictionary join molecule_synonyms on molecule_dictionary.molregno = molecule_synonyms.molregno;'

#"WHERE TYPE = 'table' AND name = 'chembl_id_lookup'"
#print(SQLITE_SELECT_TEXT)

#select * from molecule_dictionary join molecule_synonyms on molecule_dictionary.molregno = molecule_synonyms.molregno


def get_data(db_str=None , sqlite_str=None):
    """Gets the source data.

    :param db_str string: path to sqlite database file
    :param sqlite_str string: SQL query command that will be executed
    :return: A data frame containing the original source data
    :rtype: pandas.DataFrame
    """
    db_str = CHEMBL_DB if db_str is None else db_str
    sqlite_str = SQLITE_SELECT_TEXT if sqlite_str is None else sqlite_str
    print(sqlite_str + ' __IN_ ' + CHEMBL_DB)
    db = sqlite3.connect(db_str)
    df = pd.read_sql_query(sqlite_str, db)
    return df

def write_chemical_belns(file, df=None):
    """Writes the Entities as a BEL namespace file.

    :param file file: A writable file or file-like
    :param pandas.DataFrame df: A data frame containing the original data source
    """


if __name__ == "__main__":
    df = get_data(CHEMBL_DB, test_query)
    print(df.head())