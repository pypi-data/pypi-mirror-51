import sys
import re
import copy
import pprint
import json

import click
from pyzabbix import ZabbixAPI
from bullet import Check

from .command import hosts
from ..zabbix_ctl import ZabbixCTL
from ..utils import validate_match, validate_json, check_dry_run


def get_interfaces(zapi, _filter=None, match=None):
    """
    
    Parameters
    ----------
    zapi: ZabbixAPI
        ZabbixAPI object
    _filter: dict
        Must include hostid and host key.
    match: [dict]
        All items in the dict are chained "and" operator.
        All dict are chained "or" operator.
    Returns
    -------
    match_itf
    """
    if _filter is not None and ('hostid' not in _filter or 'host' not in _filter):
        raise ValueError('filter must include hostid and host key.')

    _interfaces = zapi.hostinterface.get(filter=_filter)
    if _filter is not None:
        for itf in _interfaces:
            # hostid is already included. No need hostid.
            itf['host'] = _filter['host']

    if match is None:
        return _interfaces

    ret = []
    for m in match:
        match_itf = copy.deepcopy(_interfaces)
        for k, v in m.items():
            match_itf = list(
                filter(
                    lambda _itf: re.search(v, _itf[k]) is not None,
                    match_itf,
                )
            )

        ret.extend(match_itf)

    return ret


def update_interfaces(zapi, _interfaces, data):
    """

    Parameters
    ----------
    zapi: ZabbixAPI
    _interfaces: list
    data: dict

    Returns
    -------
    interfaceids: list
        list of ids

    """
    interfaceids = []
    for itf in _interfaces:
        interfaceid = zapi.hostinterface.update(interfaceid=itf['interfaceid'], **data)
        interfaceids.append(interfaceid)

    return interfaceids


def ask_interfaces(_interfaces):
    """

    Parameters
    ----------
    _interfaces

    Returns
    -------

    """
    click.echo('\n')  # terminal new line
    choices = [f'dns[{itf["dns"]}], ip[{itf["ip"]}]' for itf in _interfaces]
    select_interfaces_cli = Check(
        prompt=f"Choose interfaces: input <space> to choose, then input <enter> to finish",
        choices=choices,
        align=4,
        margin=1,
    )
    selected_interfaces = select_interfaces_cli.launch()
    selected_interfaces = list(
        filter(
            lambda itf: f'dns[{itf["dns"]}], ip[{itf["ip"]}]' in selected_interfaces,
            _interfaces,
        ),
    )
    return selected_interfaces


@hosts.group()
@click.option('-m', '--match',
              callback=validate_match,
              help=('For search host by regex. Using re.search() in python. \n'
                    'You can use json.\n'
                    'ex1) \'{"hostid": "^111$"}\' -> This matches 111\n'
                    'ex2) \'{"interfaceid": 41}\' -> This matches 4123232, 111141, ...'
                    'ex3) \'{"dns": "^$"}\' -> This matches empty string')
              )
@click.pass_obj
def interfaces(obj, match):
    """
    Entry point interfaces command.
    Get host interfaces.

    Parameters
    ----------
    obj: ZabbixCTL
        ZabbixCTL object
    match: list
        pattern matches

    """

    _interfaces = []
    for host in obj.hosts:
        _filter = {'host': host['host'], 'hostid': host['hostid']}
        _interfaces.extend(get_interfaces(obj.zapi, _filter=_filter, match=match))

    obj.interfaces = _interfaces


@interfaces.command(name='list', help='list interfaces')
@click.pass_obj
def _list(obj):
    """

    Parameters
    ----------
    obj: ZabbixCTL

    """
    click.echo(f'{json.dumps({"interfaces": obj.interfaces})}')


@interfaces.command(help='update interfaces')
@click.option('-d', '--data', callback=validate_json)
@click.option('-y', '--yes', default=False, is_flag=True,
              help=('Turn on yes mode.\n'
                    'No confirmation update or delete.'))
@click.pass_obj
@check_dry_run
def update(obj, data, yes):
    """

    Parameters
    ----------
    obj: ZabbixCTL
    data: dict
        new data. json like object.
    yes: bool
        If yes is true, no confirmation update or delete.

    """
    if obj.main_options['interactive']:
        selected_interfaces = ask_interfaces(obj.interfaces)
    else:
        selected_interfaces = obj.interfaces

    if len(selected_interfaces) == 0:
        click.echo(f'{json.dumps({"message": "There is not host."})}')
        sys.exit()

    if yes or click.confirm(
            (f'update interfaceids: {pprint.pformat([itf["interfaceid"] for itf in selected_interfaces])}\n'
             f'data: {pprint.pformat(data)}'),
            default=False,
            abort=True,
            show_default=True):
        result = update_interfaces(obj.zapi, selected_interfaces, data)
        click.echo(f'{json.dumps(result)}')


@interfaces.command(help='change from use ip -> use dns')
@click.option('-y', '--yes', default=False, is_flag=True,
              help=('Turn on yes mode.\n'
                    'No confirmation update or delete.'))
@click.pass_obj
@check_dry_run
def usedns(obj, yes):
    """
    Update host interfaces from use ip -> use dns.

    Parameters
    ----------
    obj: ZabbixCTL
        ZabbixCTL object
    yes: bool
        If yes is true, no confirmation update or delete.

    """
    # ignore interface which dns is empty string
    formatted_interfaces = list(filter(lambda itf: len(itf['dns']) > 0, obj.interfaces))

    if obj.main_options['interactive']:
        selected_interfaces = ask_interfaces(formatted_interfaces)
    else:
        selected_interfaces = formatted_interfaces

    if len(selected_interfaces) == 0:
        click.echo(f'{json.dumps({"message": "There is no interface."})}')
        sys.exit(0)

    if yes or click.confirm(
            f'usedns: interfaceids{pprint.pformat([itf["interfaceid"] for itf in selected_interfaces])}\n',
            default=False,
            abort=True,
            show_default=True):
        result = update_interfaces(obj.zapi, selected_interfaces, {'useip': 0})
        click.echo(f'{json.dumps(result)}')
