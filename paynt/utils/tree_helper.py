
import os
import json

from math import floor

import logging
logger = logging.getLogger(__name__)


def build_tree_helper(tree_node_json, helper=[], parent=None):
    current_index = len(helper)
    if tree_node_json['split'] is None:
        # TODO this is a temp fix that only works for some models...
        helper.append({'id': current_index, 'leaf': True, 'chosen': tree_node_json['actual_label'], 'parent': parent})
        return helper
    helper.append({'id': current_index, 'leaf': False, 'chosen': (tree_node_json['split']['lhs']['var'], floor(tree_node_json['split']['rhs'])), 'children': [], 'evaluations': {(x['split']['lhs']['var'], floor(x['split']['rhs'])): x['impurity'] for x in tree_node_json['additional_splits']}, 'parent': parent})
    # sort the evaluations by impurity value
    helper[current_index]['evaluations'] = {k: v for k, v in sorted(helper[current_index]['evaluations'].items(), key=lambda item: item[1])}

    assert len(tree_node_json['children']) == 2, "expected two children"
    # left child
    assert tree_node_json['children'][0]['edge_label'] == "true", "expected left child edge label to be True"
    helper[current_index]['children'].append(len(helper))
    helper = build_tree_helper(tree_node_json['children'][0], helper, current_index)
    # right child
    assert tree_node_json['children'][1]['edge_label'] == "false", "expected right child edge label to be False"
    helper[current_index]['children'].append(len(helper))
    helper = build_tree_helper(tree_node_json['children'][1], helper, current_index)

    return helper

def parse_tree_helper(tree_helper_path):
    with open(tree_helper_path, 'r') as file:
        tree_helper = json.load(file)
    tree_helper =  build_tree_helper(tree_helper, [])
    return tree_helper
