# coding=utf-8

import ibis
import copy

from .util import register_builtin


@ibis.filters.register('get')
def get_attr(obj, attr):
    return obj.get(attr)


@ibis.filters.register('resolve')
@register_builtin('resolve')
def resolve_variable(arg):
    return ibis.nodes.ResolveContextVariable(arg)


@ibis.filters.register('merge_dict')
@ibis.filters.register('merge')
@register_builtin('merge')
def merge_dict(*args):
    final_dict = {}
    for arg in args:
        final_dict.update(copy.deepcopy(arg))

    return final_dict
