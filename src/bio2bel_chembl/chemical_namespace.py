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

#"WHERE TYPE = 'table' AND name = 'chembl_id_lookup'"
#print(SQLITE_SELECT_TEXT)

#select * from molecule_dictionary join molecule_synonyms on molecule_dictionary.molregno = molecule_synonyms.molregno


def get_data(db_str ,sqlite_str):
    """Gets the source data.

    :param db_str string: path to sqlite database file
    :param sqlite_str string: SQL query command that will be executed
    :return: A data frame containing the original source data
    :rtype: pandas.DataFrame
    """
    print(sqlite_str)
    db = sqlite3.connect(db_str)
    df = pd.read_sql_query(SQLITE_SELECT_TEXT, db)
    return df

if __name__ == "__main__":
    df = get_data(CHEMBL_DB, SQLITE_SELECT_TEXT)
    print(df.head())