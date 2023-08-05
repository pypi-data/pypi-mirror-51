import pprint
import json


class ZabbixCTL(object):
    def __init__(self, zapi, hosts=None, graphs=None, interfaces=None, **kwargs):
        self.zapi = zapi
        self.hosts = hosts
        self.graphs = graphs
        self.interfaces = interfaces
        self.main_options = kwargs

    def __repr__(self):
        zctl_json = json.dumps({
            'zabbxctl_options': self.main_options,
            'hosts': self.hosts,
            'graphs': self.graphs,
            'interfaces': self.interfaces,
        })
        return f'{zctl_json}'
