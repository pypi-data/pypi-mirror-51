from click import Context

from .utils import *


@click.group(help=('Entry point.\n'
                   'Initialize ZabbixAPI.'),
             invoke_without_command=True,
             )
@click.option('-aa', '--apiserver-address', default='http://localhost:8081',
              help=('Zabbix api server address.\n'
                    'ex) http://localhost:8081')
              )
@click.option('-u', '--username', default='Admin', help='Zabbix username')
@click.option('-p', '--password', default='zabbix', help='Zabbix password')
@click.option('-bu', '--basicauth-username', default=None, help='Basic authentication username')
@click.option('-bp', '--basicauth-password', default=None, help='Basic authentication password')
@click.option('--dry-run', default=False, is_flag=True,
              help=('Activate debug mode.\n'
                    'Create, Update, Delete API are not executed.\n'
                    'Only Get API is executed.'))
@click.option('-i', '--interactive', default=False, is_flag=True,
              help=('Turn on interactive mode.\n'
                    'Confirmation is still available.'))
@click.option('--called', default='cli', help='This option is for flask.')
@click.option('-v', '--version', default=False, is_flag=True)
@click.pass_context
def main(
        ctx,
        apiserver_address,
        username, password,
        basicauth_username, basicauth_password,
        dry_run,
        interactive,
        called,
        version,
):
    """
    Initialize ZabbixCTL

    Parameters
    ----------
    ctx: Context
        click context
    apiserver_address: str
        api server address
    username: str
        login username
    password: str
        login password
    basicauth_username: str
        basic auth username
    basicauth_password: str
        basic auth password
    dry_run: bool
        dry run option is on or off
        This is only available in cli.
    interactive: bool
        interactive option is on or off.
        This is only available in cli.
    called: str
        cli or http
    version: bool
        flag for --version
    Returns
    -------

    """
    if version or ctx.invoked_subcommand is None:
        from . import VERSION
        click.echo(f'zabbixctl {VERSION}')
        sys.exit()
    else:
        zapi = zabbix_auth(apiserver_address, username, password, basicauth_username, basicauth_password)
        ctx.obj = ZabbixCTL(zapi, dry_run=dry_run, interactive=interactive, called=called)
