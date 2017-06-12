# -*- coding: utf-8 -*-


def get_hgnc_chembl_mapping(graph):
    """Returns a mapping of HGNC proteins in a graph to ChEMBL

    1. Get all proteins from HGNC using :func:`pybel_tools.selection.get_nodes_by_function_namespace`
    2. Either download a mapping from somewhere, or load up a cached copy from a data directory like
       ``~/.pybel/data/bio2bel/chembl`` OR use a web resolving service
    3. Do magic

    :param pybel.BELGraph graph: A BEL graph
    :return: A dictionary from HGNC names to ChEMBL names
    :rtype: dict[str, str]
    """
    raise NotImplementedError


def get_associations(graph):
    """This function takes a BEL graph and finds related data from ChEMBL

    1. identify all proteins in the graph
    2. search ChEMBL for all activities of these proteins using the ChEMBL `python client <https://github.com/chembl/chembl_webresource_client>`_
    3. Return a list with tuples of (protein, chemical, activity-type, relation, standard value, standard units)

    :param pybel.BELGraph graph: A BEL graph
    :rtype: list[tuple]
    """
    raise NotImplementedError


def enrich_graph(graph):
    """Call on previous methods to get the inhibition data, then load it as edges in the BEL graph.

    :param pybel.BELGraph graph: A BEL graph
    """
    raise NotImplementedError
