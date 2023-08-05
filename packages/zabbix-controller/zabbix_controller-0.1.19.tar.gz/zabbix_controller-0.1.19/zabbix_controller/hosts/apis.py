import copy
import re

from pyzabbix import ZabbixAPI


def get_hosts(zapi, match=None, time_range=None):
    """
    Get hosts matching 'match' and 'time_range'

    Parameters
    ----------
    zapi: ZabbixAPI
    match: [dict]
        Regex. Using re package. These conditions are chained by `and` operator.
        Not Used for API requests.
        Used after API requests.
        [{'name': 'some_name', 'hostid': '^1234'}, {'name': 'other_name'}]
        All items in the dict are chained "and" operator.
        All dict are chained "or" operator.
        (name match some_name and hostid match ^1234) or name match other_name

    time_range: dict
        {'key': 'error_from', 'from': 0, 'to': int(time.time())}

    Returns
    -------
    hosts: [dict]
        list of host object.
    """

    hosts = zapi.host.get()

    if match is not None:
        match_hosts = []
        for m in match:
            hosts_copy = copy.deepcopy(hosts)
            for k, v in m.items():
                hosts_copy = list(
                    filter(
                        lambda _host: re.search(v, _host[k]) is not None,
                        hosts_copy,
                    )
                )

            match_hosts.extend(hosts_copy)

        match_hosts = list({v['hostid']: v for v in match_hosts}.values()) # unique

    else:
        match_hosts = copy.deepcopy(hosts)

    if time_range is not None:
        ret = list(filter(
            lambda host: time_range['from'] <= int(host[time_range['key']]) <= time_range['to'],
            match_hosts,
        ))

    else:
        ret = match_hosts

    return ret


def update_hosts(zapi, hosts, data):
    """
    update host

    Parameters
    ----------
    zapi: ZabbixAPI
        ZabbixAPI object
    hosts: [dict]
        list of host object
    data: dict
        new data

    Returns
    -------
    results: list
    """
    results = []
    for host in hosts:
        result = zapi.host.update(hostid=host['hostid'], **data)
        results.append(result)

    return results
