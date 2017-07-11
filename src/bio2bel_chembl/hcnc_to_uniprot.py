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

HGNC_UNIPROT_URL = 'http://www.genenames.org/cgi-bin/download?col=gd_app_sym&col=md_prot_id&status=Approved&status_opt=2&where=&order_by=gd_app_sym_sort&format=text&limit=&hgnc_dbtag=on&submit=submit'

def get_data():
    """Gets the source data.

    :return: A data frame containing the original source data
    :rtype: pandas.DataFrame
    """
    df = pd.read_csv(
        HGNC_UNIPROT_URL,
        skiprows=1,
        sep="\t",
        names=['hgnc_id', 'uniprot_id']
    )
    return df

def write_hgnc_protein_families(file, df=None):
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
            'UNIPROT': 'n/a',
            'CHEMBLP': 'n/a',
        },
        namespace_patterns={},
        annotations_dict={},
        annotations_patterns={},
        file=file
    )

    print('SET Citation = {{"URL","{}"}}'.format(HGNC_UNIPROT_URL), file=file)
    print('SET Evidence = "HGNC to UniProt mapping"', file=file)

    for _,hgnc_id, uniprot_id in df[['hgnc_id', 'uniprot_id']].itertuples():
        uniprot_clean = ensure_quotes(str(uniprot_id).strip())
        hgnc_clean = ensure_quotes(str(hgnc_id).strip())

        print('p(UNIPROT:{}) eq p(HGNC:{})'.format(uniprot_clean, hgnc_clean), file=file)


if __name__ == '__main__':
    df = get_data()
    with open(os.path.join(CHEMBL_DATA_DIR, 'HGNC_UNIPROT_MAPPING.bel'), 'w') as file:
        write_hgnc_protein_families(file, df=df)
