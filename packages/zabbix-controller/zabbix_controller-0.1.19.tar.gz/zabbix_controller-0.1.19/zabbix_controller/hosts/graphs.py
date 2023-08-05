import re
import pprint
import json
import copy
import sys

import click
from pyzabbix import ZabbixAPI

from .command import hosts
from ..utils import validate_match, check_dry_run, ask_graphs
from . import ZabbixCTL


def get_graphs(zapi, _filter=None, match=None):
    """
    Get graphs.

    Add hostid, host property in graph dict.

    Parameters
    ----------
    zapi: ZabbixAPI
        ZabbixAPI object
    _filter: dict
        Must include host key that is hostname.
        {'name': 'some-name'}.
        Not regex. Used for API requests.
    match: [dict]
        Regex. Using re package. These conditions are chained by `and` operator.
        Not Used for API requests.
        Used after API requests.
        All items in the dict are chained "and" operator.
        All dict are chained "or" operator.
        (name match some_name and hostid match ^1234) or name match other_name

    Returns
    -------
    _graphs: [dict]
        graph objects including host
    """
    if _filter is not None and 'host' not in _filter:
        raise ValueError('filter must include host key.')

    _graphs = zapi.graph.get(filter=_filter)

    if _filter is not None:
        for g in _graphs:
            g['host'] = _filter['host']

    if match is not None:
        match_graphs = []
        for m in match:
            graphs_copy = copy.deepcopy(_graphs)
            for k, v in m.items():
                graphs_copy = list(
                    filter(
                        lambda _graph: re.search(v, _graph[k]) is not None,
                        graphs_copy,
                    )
                )

            match_graphs.extend(graphs_copy)

        match_graphs = list({v['graphid']: v for v in match_graphs}.values())  # unique

    else:
        match_graphs = copy.deepcopy(_graphs)

    return match_graphs


@hosts.group(help='host graph')
@click.option('-m', '--match',
              callback=validate_match,
              help=('For search host by regex. Using re.search() in python. \n'
                    'You can use json.\n'
                    'ex1) \'{"name": "^some$"}\' -> This matches some\n'
                    'ex2) \'{"graphid": 41}\' -> This matches 4123232, 111141, ...'
                    'ex3) \'{"name": "^$"}\' -> This matches empty string')
              )
@click.pass_obj
def graphs(obj: ZabbixCTL, match):
    """
    Entry point graphs command. Add graphs to ZabbixCTL.
    graphs = [{hostname: 'host_name', graphs: [graph]}]
    """

    _graphs = []
    for host in obj.hosts:
        h_graphs = get_graphs(obj.zapi, {'host': host['host']}, match=match)
        if len(h_graphs) == 0:
            continue

        _graphs.extend(h_graphs)

    obj.graphs = _graphs


@graphs.command(name='list', help='list graph')
@click.pass_obj
def _list(obj):
    click.echo(f'{json.dumps({"graphs": obj.graphs})}')


@graphs.command(help='delete graph')
@click.option('-y', '--yes', default=False, is_flag=True,
              help=('Turn on yes mode.\n'
                    'No confirmation update or delete.'))
@click.pass_obj
@check_dry_run
def delete(obj, yes):
    """

    Parameters
    ----------
    obj: ZabbixCTL
    yes: bool
        If yes is true, no confirmation update or delete.

    Returns
    -------

    """
    if obj.main_options['interactive']:
        selected_graphs = ask_graphs(obj.graphs)
    else:
        selected_graphs = obj.graphs

    if len(selected_graphs) == 0:
        click.echo(f'{json.dumps({"message": "There is no graph."})}')
        sys.exit(0)

    if yes or click.confirm(
            f'delete:\n{pprint.pformat([(graph["host"], graph["name"]) for graph in selected_graphs])}',
            default=False,
            abort=True,
            show_default=True):
        obj.zapi.graph.delete(*[graph['graphid'] for graph in selected_graphs])
