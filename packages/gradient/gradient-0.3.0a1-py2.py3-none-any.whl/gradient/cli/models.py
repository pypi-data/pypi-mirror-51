import click

from gradient.cli import common
from gradient.cli.cli import cli
from gradient.commands import models as models_commands


@cli.group("models", help="Manage models", cls=common.ClickGroup)
def models_group():
    pass


@models_group.command("list", help="List models with optional filtering")
@click.option(
    "--experimentId",
    "experiment_id",
    help="Use to filter by experiment ID",
)
@click.option(
    "--projectId",
    "project_id",
    help="Use to filter by project ID",
)
@common.api_key_option
def list_models(api_key, experiment_id, project_id):
    command = models_commands.ListModelsCommand(api_key=api_key)
    command.execute(experiment_id=experiment_id, project_id=project_id)
