import os
import unittest

from bio2bel_chembl.chemical_inhibitions import get_data

dir_path = os.path.dirname(os.path.realpath(__file__))
test_db_path = os.path.join(dir_path, 'chembl23_test.db')

SQLITE_SELECT_TEXT = """
select target_dictionary.chembl_id as chembl_target_p , chembl_molecule_id
from target_dictionary join
(select chembl_molecule_id, tid
from assays join
(select molecule_dictionary.chembl_id as chembl_molecule_id, molregno, activity_id, assay_id
from molecule_dictionary join ( select molregno, activity_id, assay_id
								from activities
								where standard_type = 'IC50' and standard_value <= 10000)
						 using (molregno) ) using (assay_id)) using (tid);
"""


class TestTree(unittest.TestCase):
    def setUp(self):
        self.df = get_data(test_db_path, SQLITE_SELECT_TEXT)

    def test_lenght(self):
        """tests the lenght of the df"""
        self.assertEqual(12, len(self.df))
    def test_values(self):
        """check if data is there"""
        self.assertIn('CHEMBL273', self.df.values)
        self.assertIn('CHEMBL56', self.df.values)
        self.assertIn('CHEMBL2093870', self.df.values)
        self.assertIn('CHEMBL41', self.df.values)


if __name__ == '__main__':
    unittest.main()