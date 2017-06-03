# -*- coding: utf-8 -*-

from mosql import query, mysql, util  # @UnusedImport

# 将data数据插入字典中，若不指定key,则插入data中所有数据
def insert(table, data , keys=None):
    if keys:
        if type(data) == list:
            vals = []
            for obj in data:
                vals.append([v for k, v in obj if k in keys])
        else:
            vals = [v for k, v in data if k in keys]
        return query.insert(table, columns=keys, values=vals)
    else:
        return query.insert(table, data)

def multi_insert(table, datas , keys=None):
    if not keys:
        keys = datas[0].keys
    pair = dict(zip(keys, ["%s"] * len(keys)))
    params = [[data[key] for key in keys] for data in datas]
    return query.insert(table, pair), params


def update(table, data, where=None, keys=None):
    if keys:
        data = {key:data[key] for key in keys}
    return query.update(table, where=where, set=data)

def multiUpdate(table, datas, where=None, keys=None):
    if not keys:
        keys = datas[0].keys()
    pair = dict(zip(keys, ["%s"] * len(keys)))
    params = [[data[key] for key in keys] for data in datas]
    return query.update(table, pair), params

def join(table, on=None, using=None, _type='left'):
    return query.join(table, on=on, using=using, type=_type)

def select(table, columns=None, where=None, joins=None, order=None, group=None, limit=None, offset=None):
    return query.select(table, columns=columns, where=where, joins=joins, order_by=order, group_by=group, limit=limit, offset=offset)

def delete(table, where):
    return query.delete(table, where)

def sqlAnd(where, conmap={}, keys=None):
    new_dict = {}
    if not keys:
        keys = where.keys()
    for key in keys:
        if key in conmap:
            new_dict[(key, conmap[key])] = where[key]
        else:
            new_dict[key] = where[key]
    return util.build_where(new_dict)

def sqlOr(where, conmap={}, keys=None, andpart=None):
    new_list = []
    if not keys:
        keys = where.keys()
    for key in keys:
        if key in conmap:
            new_list.append({(key, conmap[key]):where[key]})
        else:
            new_list.append({key:where[key]})
    if andpart:
        new_list.append(andpart)
    return util.or_(new_list)

def raw(string):
    return util.value(util.raw(string))

def value(value):
    return util.value(value)
