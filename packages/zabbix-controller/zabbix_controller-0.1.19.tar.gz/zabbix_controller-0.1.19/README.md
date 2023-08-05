# 1. Zabbix CLI
## 1.1 Example
### 1.1.1 Valid Command
```bash
zabbix_controller -u username -p password hosts list
zabbix_controller -u username -p password hosts -m name:^server$ list
```

### 1.1.2 Invalid Command
```bash
zabbix_controller hosts -u username -p password list
zabbix_controller -u username -p password hosts list -m name:^server$
```

## 1.2 zabbixctl [options] command ...
### 1.2.1 Options
These options are only set at `zabbixctl [options] command ...`.
`zabbixctl command [options] ...` is not accepted.
#### 1.2.1.1 --help
```bash
zabbixctl --help
```
#### 1.2.1.2 --apiserver-address, -aa
```bash
zabbixctl -aa http://localhost:8081
```
#### 1.2.1.3 --username, -u, --password, -p
Used for zabbix login
```bash
zabbixctl --username Admin --password zabbix_password
```
#### 1.2.1.4 --basicauth_username, -bu, --basicauth_password, -bp
Used for basic authentication
```bash
zabbixctl -bu alis -bp alis_password
```
#### 1.2.1.5 --dry-run
If you set `--dry-run`, only get API is executed, then ZabbixCTL state is printed.
Create, update, delete like API is not executed.
```bash
zabbixctl --dry-run
```

## 1.3 zabbixctl host `Options` `Command` ...
### 1.3.1 Options
#### 1.3.1.1 `-m, --match`
Search host using json like object.
Search key, then apply value.
In the example below, 
hosts which name key is including `some_name` are listed.
```bash
zabbixctl hosts -m '{"name": "some_name"}' list
zabbixctl hosts -m '[{"name": "some_name"}]' list
```
Each key, value pairs are chained by `and operator`.
Each dicts are chained by `or operator`.

This command mean `("name": "some_name" and "hostid": "^1") or "name": "other_name"`.
```bash
zabbixctl hosts -m '[{"name": "some_name", "hostid": "^1"}, {"name": "other_name"}]' list
```

#### 1.3.1.2 `-tr, --time-range`
This option is able to specify time range.
If you use --match at the same time, used by "and operator".
```
key:[from]-[to]
```
`from` and `to` must be unixtime and can be omitted.
These commands are same and print host which disable property is included from 0 to now.
```bash
zabbixctl hosts -tr disable:0- list
zabbixctl hosts -tr disable:- list
```
This command mean `(("name": "some_name" and "hostid": "^1") or "name": "other_name") and (0 <= disable_until <= now)`.
```bash
zabbixctl hosts -m '[{"name": "some_name", "hostid": "^1"}, {"name": "other_name"}]' -tr 'disable_until:-' list
```


### 1.3.2 Commands
#### 1.3.2.1 `list`
list up host
#### 1.3.2.2 `delete`
delete host
- options
    - `-y, --yes`
```bash
zabbixctl hosts -m '{"name": "some_name"}' delete -y
```
#### 1.3.2.3 `disable`
disable host
- options
    - `-y, --yes`
```bash
zabbixctl hosts -m '{"name": "some_name"}' disable -y
```
#### 1.3.2.4 `update`
update host
- options
    - `-d, --data`
    - `-y, --yes`

These are same command.
```bash
zabbixctl hosts -m '{"name": "some_name"}' update -d '{"state": 1}' -y
zabbixctl hosts -m '{"name": "some_name"}' update -d '{"state": "1"}' -y
zabbixctl hosts -m '{"name": "some_name"}' disable -y
```

## 1.4 zabbixctl host graphs `Options` `Command`
### 1.4.1 Command
#### 1.4.2 `list`
#### 1.4.3 `delete`
- options
    - `-y, --yes`
### 1.4.2 Options
#### 1.4.2.1 `-m, --match`

This command delete graphs which is in hosts which is matched regex.
```bash
zabbixctl hosts -m '{"name": "some_name"}' graphs delete -y
```

## 1.5 zabbixctl host interfaces `Options` `Command`
### 1.5.1 Command
#### 1.5.1.1 `list`
#### 1.5.1.2 `usedns`
Use dns, not ipaddress
- options
    - `-y, --yes`

#### 1.5.1.3 `update`
These are same command.
- options
    - `-y, --yes`
```bash
zabbixctl hosts interfaces update -d '{"useip": 0}' -y
zabbixctl hosts interfaces update -d '{"useip": "0"}' -y
zabbixctl hosts interfaces usedns -y
```
# LICENSE
