# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['zabbix_controller', 'zabbix_controller.hosts']

package_data = \
{'': ['*']}

install_requires = \
['bullet>=2.1,<3.0', 'click>=7.0,<8.0', 'pyzabbix>=0.7.5,<0.8.0']

entry_points = \
{'console_scripts': ['zabbixctl = zabbix_controller.call_command:call_command']}

setup_kwargs = {
    'name': 'zabbix-controller',
    'version': '0.1.19',
    'description': '',
    'long_description': '# 1. Zabbix CLI\n## 1.1 Example\n### 1.1.1 Valid Command\n```bash\nzabbix_controller -u username -p password hosts list\nzabbix_controller -u username -p password hosts -m name:^server$ list\n```\n\n### 1.1.2 Invalid Command\n```bash\nzabbix_controller hosts -u username -p password list\nzabbix_controller -u username -p password hosts list -m name:^server$\n```\n\n## 1.2 zabbixctl [options] command ...\n### 1.2.1 Options\nThese options are only set at `zabbixctl [options] command ...`.\n`zabbixctl command [options] ...` is not accepted.\n#### 1.2.1.1 --help\n```bash\nzabbixctl --help\n```\n#### 1.2.1.2 --apiserver-address, -aa\n```bash\nzabbixctl -aa http://localhost:8081\n```\n#### 1.2.1.3 --username, -u, --password, -p\nUsed for zabbix login\n```bash\nzabbixctl --username Admin --password zabbix_password\n```\n#### 1.2.1.4 --basicauth_username, -bu, --basicauth_password, -bp\nUsed for basic authentication\n```bash\nzabbixctl -bu alis -bp alis_password\n```\n#### 1.2.1.5 --dry-run\nIf you set `--dry-run`, only get API is executed, then ZabbixCTL state is printed.\nCreate, update, delete like API is not executed.\n```bash\nzabbixctl --dry-run\n```\n\n## 1.3 zabbixctl host `Options` `Command` ...\n### 1.3.1 Options\n#### 1.3.1.1 `-m, --match`\nSearch host using json like object.\nSearch key, then apply value.\nIn the example below, \nhosts which name key is including `some_name` are listed.\n```bash\nzabbixctl hosts -m \'{"name": "some_name"}\' list\nzabbixctl hosts -m \'[{"name": "some_name"}]\' list\n```\nEach key, value pairs are chained by `and operator`.\nEach dicts are chained by `or operator`.\n\nThis command mean `("name": "some_name" and "hostid": "^1") or "name": "other_name"`.\n```bash\nzabbixctl hosts -m \'[{"name": "some_name", "hostid": "^1"}, {"name": "other_name"}]\' list\n```\n\n#### 1.3.1.2 `-tr, --time-range`\nThis option is able to specify time range.\nIf you use --match at the same time, used by "and operator".\n```\nkey:[from]-[to]\n```\n`from` and `to` must be unixtime and can be omitted.\nThese commands are same and print host which disable property is included from 0 to now.\n```bash\nzabbixctl hosts -tr disable:0- list\nzabbixctl hosts -tr disable:- list\n```\nThis command mean `(("name": "some_name" and "hostid": "^1") or "name": "other_name") and (0 <= disable_until <= now)`.\n```bash\nzabbixctl hosts -m \'[{"name": "some_name", "hostid": "^1"}, {"name": "other_name"}]\' -tr \'disable_until:-\' list\n```\n\n\n### 1.3.2 Commands\n#### 1.3.2.1 `list`\nlist up host\n#### 1.3.2.2 `delete`\ndelete host\n- options\n    - `-y, --yes`\n```bash\nzabbixctl hosts -m \'{"name": "some_name"}\' delete -y\n```\n#### 1.3.2.3 `disable`\ndisable host\n- options\n    - `-y, --yes`\n```bash\nzabbixctl hosts -m \'{"name": "some_name"}\' disable -y\n```\n#### 1.3.2.4 `update`\nupdate host\n- options\n    - `-d, --data`\n    - `-y, --yes`\n\nThese are same command.\n```bash\nzabbixctl hosts -m \'{"name": "some_name"}\' update -d \'{"state": 1}\' -y\nzabbixctl hosts -m \'{"name": "some_name"}\' update -d \'{"state": "1"}\' -y\nzabbixctl hosts -m \'{"name": "some_name"}\' disable -y\n```\n\n## 1.4 zabbixctl host graphs `Options` `Command`\n### 1.4.1 Command\n#### 1.4.2 `list`\n#### 1.4.3 `delete`\n- options\n    - `-y, --yes`\n### 1.4.2 Options\n#### 1.4.2.1 `-m, --match`\n\nThis command delete graphs which is in hosts which is matched regex.\n```bash\nzabbixctl hosts -m \'{"name": "some_name"}\' graphs delete -y\n```\n\n## 1.5 zabbixctl host interfaces `Options` `Command`\n### 1.5.1 Command\n#### 1.5.1.1 `list`\n#### 1.5.1.2 `usedns`\nUse dns, not ipaddress\n- options\n    - `-y, --yes`\n\n#### 1.5.1.3 `update`\nThese are same command.\n- options\n    - `-y, --yes`\n```bash\nzabbixctl hosts interfaces update -d \'{"useip": 0}\' -y\nzabbixctl hosts interfaces update -d \'{"useip": "0"}\' -y\nzabbixctl hosts interfaces usedns -y\n```\n# LICENSE\n',
    'author': 'hamadakafu',
    'author_email': 'kafu.h1998@gmail.com',
    'url': 'https://github.com/hamadakafu/zabbix-controller',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
