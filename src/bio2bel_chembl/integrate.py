# -*- coding: utf-8 -*-

def get_associations(graph):
    """This function takes a BEL graph and finds related data from ChEMBL

    1. identify all proteins in the graph
    2. search ChEMBL for all activities of these proteins using the ChEMBL `python client <https://github.com/chembl/chembl_webresource_client>`_
    3. Return a list with tuples of (protein, chemical, activity-type, relation, statndard value, standard units)

    :param pybel.BELGraph graph:
    :rtype: list[tuple]
    """
    raise NotImplementedError
