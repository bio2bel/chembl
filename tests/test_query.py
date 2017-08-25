import os
import unittest

from bio2bel_chembl.chemical_namespace import get_data

dir_path = os.path.dirname(os.path.realpath(__file__))
test_db_path = os.path.join(dir_path, 'chembl23_test.db')

SQLITE_SELECT_TEXT = """
select 
  chembl_id
from molecule_dictionary
"""

class TestTree(unittest.TestCase):
    def setUp(self):
        self.df = get_data(test_db_path, SQLITE_SELECT_TEXT)

    def test_lenght(self):
        """tests the lenght of df"""
        self.assertEqual(12000, len(self.df))

    def test_components(self):
        """tests if several components are in df"""
        self.assertIn('CHEMBL100', self.df.values)
        self.assertIn('CHEMBL8122', self.df.values)
        self.assertIn('CHEMBL9999', self.df.values)

if __name__ == '__main__':
    unittest.main()