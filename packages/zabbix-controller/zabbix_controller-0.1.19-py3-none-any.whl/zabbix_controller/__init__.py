# TODO: --dry-runをつかってテストできるようにする

# TODO: 本当は，gcpのインスタンスがあるかどうかのチェックをする
# TODO: zabbixにあるhostidとかhostnameと比較して，集合の差をとる (zabbix.hostname - gcp.instancename)

from . import cli
from . import utils
from . import hosts
from . import zabbix_ctl

VERSION = "0.1.19"
