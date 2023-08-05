import pprint
import json
import sys

import click

from . import main, ZabbixCTL
from ..utils import validate_match, validate_time_range, validate_json, check_dry_run, ask_hosts
from .apis import get_hosts, update_hosts


@main.group(help='host command entry point')
@click.option('-m', '--match',
              callback=validate_match,
              help=('For search host by regex. Using re.search() in python. \n'
                    'You can use json.\n'
                    'ex1) \'{"name": "^some$"}\' -> This matches some\n'
                    'ex2) \'{"hostid": "41"}\' -> This matches 4123232, 111141, ...\n'
                    'ex3) \'{"name": "^$"}\' -> This matches empty string\n'
                    'ex4) \'[{"name": "^some"}, {"hostid": "11"}]\' \n'
                    '-> name starts with "some" and hostid is including "11"')
              )
@click.option('-tr', '--time-range',
              callback=validate_time_range,
              help=('For search by time range. Using unixtime\n'
                    'key:[from]-[to].\n'
                    'If you use --match at the same time, used by "and operator".\n'
                    '"from" must be less than "to".\n'
                    'ex1) errors_from:48120471-140834017 -> 48120471~140834017\n'
                    'ex2) errors_from:- -> 0~[now unixtime]\n'
                    'ex3) disable_until:-7184 -> 0~7184\n')
              )
@click.pass_obj
def hosts(obj, match, time_range):
    """
    Parameters
    ----------
    obj: ZabbixCTL
        Including command state.
    match: dict
        Key is host property in zabbix api.
        Value is regular expresion used by re.
        Each items is chained && operator, not ||.
    time_range: dict
        Keys are 'key', 'from', 'to'.
        Values are str, int, int.
        'from' <= host['key'] <= 'to'
    """
    _hosts = get_hosts(obj.zapi, match=match, time_range=time_range)
    obj.hosts = _hosts

    if len(_hosts) == 0:
        click.echo(f'{json.dumps({"message": "There is not host."})}')
        sys.exit(0)

    obj.hosts = _hosts


@hosts.command(name='list', help='list hosts')
@click.pass_obj
def _list(obj):
    """
    List hosts.

    Parameters
    ----------
    obj: ZabbixCTL
        Including command state.
    """
    click.echo(f'{json.dumps({"hosts": obj.hosts})}')


@hosts.command(help='delete hosts')
@click.option('-y', '--yes', default=False, is_flag=True,
              help=('Turn on yes mode.\n'
                    'No confirmation update or delete.'))
@click.pass_obj
@check_dry_run
def delete(obj, yes):
    """
    Checking dry-run.
    Delete hosts.

    Parameters
    ----------
    obj: ZabbixCTL
        Including command state.
    yes: bool
        If yes is true, no confirmation update or delete.
    """
    if obj.main_options['interactive']:
        selected_hosts = ask_hosts(obj.hosts)
    else:
        selected_hosts = obj.hosts

    if len(selected_hosts) == 0:
        click.echo(f'{json.dumps({"message": "There is not host."})}')
        sys.exit(0)

    if yes or click.confirm(f'delete: {[host["name"] for host in selected_hosts]}',
                            default=False,
                            abort=True,
                            show_default=True):
        obj.zapi.host.delete(*[host['hostid'] for host in selected_hosts])


@hosts.command(help='disable hosts')
@click.option('-y', '--yes', default=False, is_flag=True,
              help=('Turn on yes mode.\n'
                    'No confirmation update or delete.'))
@click.pass_obj
@check_dry_run
def disable(obj, yes):
    """
    Checking dry-run.
    Disable hosts. It is deprecated.

    Parameters
    ----------
    obj: ZabbixCTL
    yes: bool
        If yes is true, no confirmation update or delete.
    """
    if obj.main_options['interactive']:
        selected_hosts = ask_hosts(obj.hosts)
    else:
        selected_hosts = obj.hosts

    if len(selected_hosts) == 0:
        click.echo(f'{json.dumps({"message": "There is not host."})}')
        sys.exit(0)

    if yes or click.confirm(f'disable: {pprint.pformat([host["name"] for host in selected_hosts])}',
                            default=False,
                            abort=True,
                            show_default=True):
        data = {'status': 1}
        result = update_hosts(obj.zapi, selected_hosts, data)
        click.echo(f'{json.dumps(result)}')


@hosts.command(help='update hosts')
@click.option('-d', '--data', callback=validate_json, help='data for update', required=True)
@click.option('-y', '--yes', default=False, is_flag=True,
              help=('Turn on yes mode.\n'
                    'No confirmation update or delete.'))
@click.pass_obj
@check_dry_run
def update(obj, data, yes):
    """
    Checking dry-run.
    Update hosts.

    Parameters
    ----------
    obj: ZabbixCTL
        Including command state.
    data: dict
        New data
    yes: bool
        If yes is true, no confirmation update or delete.
    """
    if obj.main_options['interactive']:
        selected_hosts = ask_hosts(obj.hosts)
    else:
        selected_hosts = obj.hosts

    if len(selected_hosts) == 0:
        click.echo(f'{json.dumps({"message": "There is not host."})}')
        sys.exit(0)

    if yes or click.confirm((f'update: {pprint.pformat([host["name"] for host in selected_hosts])}\n'
                             f'data: {pprint.pformat(data)}'),
                            default=False,
                            abort=True,
                            show_default=True):
        result = update_hosts(obj.zapi, selected_hosts, data)
        click.echo(f'{json.dumps(result)}')
