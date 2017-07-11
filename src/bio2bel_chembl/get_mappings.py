# -*- coding: utf-8 -*-

import os
import pandas as pd
from pybel.constants import PYBEL_DATA_DIR
from pybel_tools.definition_utils import write_namespace
from pybel_tools.document_utils import write_boilerplate
from pybel.constants import IS_A
from pybel.utils import ensure_quotes

CHEMBL_DATA_DIR = os.path.join(PYBEL_DATA_DIR, 'bio2bel', 'chembl')
if not os.path.exists(CHEMBL_DATA_DIR):
    os.makedirs(CHEMBL_DATA_DIR)

CHEMBL_UNIPROT_MAPPING = 'ftp://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/latest/chembl_uniprot_mapping.txt'

UNIPROT_NS_URL = 'https://arty.scai.fraunhofer.de/artifactory/bel/namespace/uniprot/uniprot-20170705.belns'
CHEMBLP_NS_URL = 'https://arty.scai.fraunhofer.de/artifactory/bel/namespace/chemblp/chemblp-20170705.belns'


def get_data():
    """Gets the source data.

    :return: A data frame containing the original source data
    :rtype: pandas.DataFrame
    """
    df = pd.read_csv(
        CHEMBL_UNIPROT_MAPPING,
        skiprows=1,
        sep="\t",
        names=['uniprot_id', 'chembl_id', 'description', 'type']
    )
    return df


def get_chemblp_names(df=None):
    """Processes the source data.

    :param pandas.DataFrame df: A data frame containing the original data source
    :return: Returns the set of current ChEMBL proteins Family names
    :rtype: set[str]
    """
    df = get_data() if df is None else df
    entries = set(df['chembl_id'].unique())
    return entries


def get_uniprot_names(df=None):
    """Processes the source data.

    :param pandas.DataFrame df: A data frame containing the original data source
    :return: Returns the set of current UniProt proteins Family names
    :rtype: set[str]
    """
    df = get_data() if df is None else df
    entries = set(df['uniprot_id'].unique())
    return entries


def write_chemblp_belns(file, df=None):
    """Writes the ChEMBL Protein Families as a BEL namespace file.

    :param file file: A writable file or file-like
    :param pandas.DataFrame df: A data frame containing the original data source
    """
    values = get_chemblp_names(df=df)

    write_namespace(
        namespace_name="ChEMBL Proteins",
        namespace_keyword="CHEMBLP",
        namespace_domain="Gene and Gene Products",
        namespace_species='9606',
        namespace_description="ChEMBL Identifiers for proteins",
        citation_name=CHEMBL_UNIPROT_MAPPING,
        author_name='Charles Tapley Hoyt',
        author_contact="charles.hoyt@scai.fraunhofer.de",
        author_copyright='Creative Commons by 4.0',
        values=values,
        functions="P",
        file=file
    )

def write_chembl_protein_families(file, df=None):
    """Writes the ChEMBL protein family hierarchy a BEL script

    :param file file: A writable file or file-like
    :param pandas.DataFrame df: A data frame containging the original data source
    """

    df = get_data() if df is None else df

    write_boilerplate(
        document_name='HGNC Gene Family Definitions',
        authors='Charles Tapley Hoyt',
        contact='charles.hoyt@scai.fraunhofer.de',
        licenses='Creative Commons by 4.0',
        copyright='Copyright (c) 2017 Charles Tapley Hoyt. All Rights Reserved.',
        description="""This BEL document represents the gene families curated by HGNC, describing various functional, structural, and logical classifications""",
        namespace_dict={
            'UNIPROT': UNIPROT_NS_URL,
            'CHEMBLP': CHEMBLP_NS_URL,
        },
        namespace_patterns={},
        annotations_dict={},
        annotations_patterns={},
        file=file
    )

    print('SET Citation = {{"URL","{}"}}'.format(CHEMBLP_NS_URL), file=file)
    print('SET Evidence = "ChEMBL to UniProt mapping"', file=file)

    for _,uniprot_id, chembl_id in df[['uniprot_id', 'chembl_id']].itertuples():
        uniprot_clean = ensure_quotes(uniprot_id.strip())
        chembl_clean = ensure_quotes(chembl_id.strip())

        print('p(UNIPROT:{}) eq p(CHEMBLP:{})'.format(uniprot_clean, chembl_clean), file=file)

def write_uniprot_belns(file, df=None):
    """Writes the UniProt Protein Families as a BEL namespace file.

    :param file file: A writable file or file-like
    :param pandas.DataFrame df: A data frame containing the original data source
    """
    values = get_uniprot_names(df=df)

    write_namespace(
        namespace_name="UniProt Proteins",
        namespace_keyword="UNIPROT",
        namespace_domain="Gene and Gene Products",
        namespace_species='9606',
        namespace_description="UniProt Identifiers for proteins",
        citation_name=CHEMBL_UNIPROT_MAPPING,
        author_name='Charles Tapley Hoyt',
        author_contact="charles.hoyt@scai.fraunhofer.de",
        author_copyright='Creative Commons by 4.0',
        values=values,
        functions="P",
        file=file
    )


if __name__ == "__main__":
    df = get_data()
    with open(os.path.join(CHEMBL_DATA_DIR, 'chemblp.belns'), 'w') as file:
        write_chemblp_belns(file, df)
    with open(os.path.join(CHEMBL_DATA_DIR, 'uniprot.belns'), 'w') as file:
        write_uniprot_belns(file, df)

    with open(os.path.join(CHEMBL_DATA_DIR, 'CHEMBL_UNIPROT_MAPPING.bel'), 'w') as file:
        write_chembl_protein_families(file, df=df)