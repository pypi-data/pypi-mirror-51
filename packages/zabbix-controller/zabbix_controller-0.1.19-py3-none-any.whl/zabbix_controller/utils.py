import sys
import time
import json
from functools import wraps

from pyzabbix import ZabbixAPI
from bullet import Check
import click

from .zabbix_ctl import ZabbixCTL


def zabbix_auth(host, username, password, basicauth_username=None, basicauth_password=None):
    """
    Authentication zabbix.

    Parameters
    ----------
    host: str
        api server address
    username: str
        login username
    password: str
        login password
    basicauth_username: str
        basic auth username
    basicauth_password: str
        basic auth password

    Returns
    -------
    ZabbixAPI
        zabbixAPI object

    """
    zapi = ZabbixAPI(host)
    if basicauth_username is not None and basicauth_password is not None:
        # Basic 認証
        zapi.session.auth = (basicauth_username, basicauth_password)
    # SLL/TLSの検証をするかどうかFalseの場合は警告メッセージが出力
    zapi.session.verify = False  # TODO: Trueにすべきかもしれない
    zapi.timeout = 5.1  # (秒)
    zapi.login(username, password)
    return zapi


def validate_match(ctx, param, values):
    """
    Parameters
    ----------
    ctx: click.Context
        click Context object
    param: click.param
        I don't know. Not using.
    values: str
        Json string. One dict must be changed [dict]. When filtering, use this, thinking this is list.
    Returns
    -------
    values: [dict]
    """
    if values is None:
        return None

    values = validate_json(ctx, param, values)
    for k, v in values.items():
        if isinstance(v, int):
            values[k] = str(v)

    if isinstance(values, dict):
        values = [values]

    if not isinstance(values, list):
        raise TypeError('logic error, must be list or dict')

    return values


def validate_time_range(ctx, param, values):
    """
    key:[unixtime]-[unixtime]
    errors_from:174134341-1841471834
    return {'key': 'errors_from', from: 174134341, to: 1841471834}
    errors_from:-
    return {'key': errors_from', from: 0, to: [now unixtime]}
    """
    if values is None:
        return None

    if ':' not in values:
        raise click.BadParameter('Please include ":" in --host-pattern. Run --help')

    k, v = values.split(':', 1)  # ignore second ':'
    f, t = v.split('-')
    # -1047 is 0-1047
    f = 0 if f == '' else int(f)
    # 71414 is 71414-[now unixtime]
    t = int(time.time()) if t == '' else int(t)
    values = {'key': k, 'from': f, 'to': t}
    return values


def validate_json(ctx, param, values):
    """
    Parameters
    ----------
    ctx: click.Context
        click Context object
    param: click.param
        I don't know. Not using.
    values: str
        Json string.
    Returns
    -------
    values: dict
    """
    if values is None:
        return None
    try:
        values = json.loads(values)
    except json.JSONDecodeError:
        raise click.BadParameter(f'You pass {values}. Please pass json format.')

    return values


def ask_hosts(hosts):
    """
    host を選択する
    return selected_hosts: [dict]
    """
    click.echo('\n')  # ターミナルをリフレッシュ

    select_hostnames_cli = Check(
        prompt="Choose instance: input <space> to choose, then input <enter> to finish",
        choices=[host['name'] for host in hosts],
        align=4,
        margin=1,
    )
    hostnames = select_hostnames_cli.launch()
    selected_hosts = list(filter(lambda host: host['name'] in hostnames, hosts))

    return selected_hosts


def ask_graphs(graphs):
    """
    1つのホストに対して行う
    return graphs: [dicts]
    """
    click.echo('\n')  # terminal new line
    choices = ['all']
    choices.extend([f'{graph["host"]}: {graph["name"]}' for graph in graphs])

    # 入力のバリデーションするのでwhile回す
    while True:
        select_graphs_cli = Check(
            prompt=f"Choose graph: input <space> to choose, then input <enter> to finish",
            choices=choices,
            align=4,
            margin=1,
        )
        selected_graphs = select_graphs_cli.launch()
        if 'all' in selected_graphs:
            if len(selected_graphs) != 1:
                # When select all, be able to select only all.
                click.echo('Select only all.')
                continue
            else:
                return graphs

        selected_graphs = list(
            filter(
                lambda graph: f'{graph["host"]}: {graph["name"]}' in selected_graphs,
                graphs,
            )
        )
        return selected_graphs


def check_dry_run(func):
    @wraps(func)
    def wrapped(obj: ZabbixCTL, *args, **kwargs):
        if obj.main_options['dry_run']:
            click.echo(f'{obj}')
            # TODO: 関数のテストの仕方を考えている...zapiが呼ばれた回数をテストすれば良さそう
            sys.exit(0)

        result = func(obj, *args, **kwargs)
        return result

    return wrapped
