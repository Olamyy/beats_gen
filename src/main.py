import os
import sys

import click

from src.helpers.user import UserContext

CONTEXT_SETTINGS = dict(auto_envvar_prefix="BEATS_GEN")

pass_config = click.make_pass_decorator(UserContext, ensure=True)
cmd_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "commands"))


class ComplexCLI(click.MultiCommand):
    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(cmd_folder):
            if filename.endswith(".py") and filename.startswith("cmd_"):
                rv.append(filename[4:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        try:
            if sys.version_info[0] == 2:
                name = name.encode("ascii", "replace")
            mod = __import__(
                "src.commands.cmd_{}".format(name), None, None, ["cli"]
            )
        except ImportError:
            return
        return mod.cli


@click.command(cls=ComplexCLI,
               context_settings=CONTEXT_SETTINGS,
               add_help_option=True)
@click.option("-v", "--verbose", is_flag=True, help="Enables verbose mode.")
@click.option("-v", "--config", help="Path to a yaml config to use")
@click.version_option()
@click.help_option()
@pass_config
def cli(ctx, verbose, config):
    """CLI application for working with zflow."""
    ctx.obj = UserContext(verbose=verbose, config_path=config)
