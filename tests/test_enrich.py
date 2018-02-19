# -*- coding: utf-8 -*-

import unittest

from bio2bel_chembl.enrich import *
from pybel import BELGraph
from pybel.dsl import abundance, protein


class TestEnrich(unittest.TestCase):
    def test_enrich_target(self):
        graph = BELGraph()
        node = graph.add_node_from_data(protein(namespace='HGNC', name='PDE5A'))

        self.assertEqual(1, graph.number_of_nodes())
        self.assertEqual(0, graph.number_of_edges())

        enrich_target(graph, node)

        self.assertLess(1, graph.number_of_nodes(), msg='should have added nodes')
        self.assertLess(0, graph.number_of_edges(), msg='should have added edges')

        # https://www.ebi.ac.uk/chembl/compound/inspect/CHEMBL779
        tadalafil = abundance(namespace='CHEBML', identifier='CHEMBL779')

        self.assertIn(tadalafil.as_tuple(), graph, msg='missing inhibitor')


if __name__ == '__main__':
    unittest.main()
