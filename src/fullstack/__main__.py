import click

from fullstack import __version__
from fullstack.config import ApplicationConfig
from fullstack.log import set_up_logging
from fullstack.service.main import start


@click.group(invoke_without_command=True)
@click.version_option(version=__version__, prog_name="fullstack")
@click.pass_context
def main(ctx: click.Context) -> None:
    config = ctx.ensure_object(ApplicationConfig)
    set_up_logging(config.logging)
    if ctx.invoked_subcommand is None:
        print("Please invoke subcommand!")


@main.command(name="serve")
@click.pass_obj
def start_application(config: ApplicationConfig):
    start(config)
