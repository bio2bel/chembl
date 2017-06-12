# -*- coding: utf-8 -*-

import unittest

from bio2bel_chembl.integrate import get_associations
from pybel import BELGraph
from pybel.constants import PROTEIN


class TestIntegrate(unittest.TestCase):
    def test_akt1(self):
        """This test checks if the entries for a given graph can be downloaded.

        The HGNC:AKT1 protein:
        - Identifier: CHEMBL4282
        - Full name: Serine/threonine-protein kinase AKT
        - Organism: Homo Sapiens
        - ChEMBL Target Report: https://www.ebi.ac.uk/chembl/target/inspect/CHEMBL4282
        - All activities: https://www.ebi.ac.uk/chembl/bioactivity/results/1/cmpd_chemblid/asc/tab/display

        One example inhibitor of HGNC:AKT1 is ELLAGIC ACID:
        - Identifier: CHEMBL6246
        - SMILES: Oc1cc2C(=O)Oc3c(O)c(O)cc4C(=O)Oc(c1O)c2c34
        - InChI Key: AFSDNFLWKVMVRB-UHFFFAOYSA-N
        - AKT1 IC50: 3340 nM

        """
        graph = BELGraph()
        graph.add_simple_node(PROTEIN, 'HGNC', 'AKT1')

        associations = set(get_associations(graph))

        ellagic_acid_entry = ('CHEMBL4282', 'CHEMBL6246', 'IC50', '=', '3340', 'nM')

        self.assertIn(ellagic_acid_entry, associations)


if __name__ == '__main__':
    unittest.main()
