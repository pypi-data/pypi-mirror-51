import zabbix_controller


def call_command():
    zabbix_controller.cli.main()


if __name__ == '__main__':
    call_command()
