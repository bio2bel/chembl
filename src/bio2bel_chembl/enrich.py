# -*- coding: utf-8 -*-

import json

from chembl_webresource_client.new_client import new_client

from pybel.constants import FUNCTION, NAME, NAMESPACE, PROTEIN
from pybel.dsl import abundance

__all__ = [
    'search_target',
    'enrich_target',
]

target = new_client.target
activities = new_client.activity


def search_target(graph, node):
    """Enriches a node with

    :param pybel.BELGraph graph: A BEL graph
    :param tuple node: A PyBEL node tuple
    :return:
    """
    data = graph.node[node]

    if data[FUNCTION] != PROTEIN:
        return

    namespace = data.get(NAMESPACE)
    if namespace is None or namespace != 'HGNC':
        return

    name = data.get(NAME)
    if name is None:
        return

    res = target.filter(target_synonym__icontains=name, target_organism__exact='Homo sapiens')

    print(json.dumps(res[0], indent=4))
    for e in res:
        print(e)

    top = res[0]
    chembl_id = top['target_chembl_id']

    return chembl_id


def enrich_target(graph, node):
    """

    :param pybel.BELGraph graph:
    :param tuple node:
    """
    target_chembl_id = search_target(graph, node)

    results = activities.filter(target_chembl_id=target_chembl_id, published_type='IC50')

    print('Activities\n')

    for act in results:
        print(json.dumps(act, indent=4))

        relation = act['standard_relation']
        value = act['standard_value']

        if relation == '=':
            if float(value) > 40000:
                continue
        else:
            print(relation)

        graph.add_inhibits(
            abundance(namespace='CHEMBL', identifier=act['']),
            node
        )


if __name__ == '__main__':
    from pybel import BELGraph
    from pybel.dsl import protein

    graph_ = BELGraph()
    node_ = graph_.add_node_from_data(protein(namespace='HGNC', name='PDE5A'))

    enrich_target(graph_, node_)
