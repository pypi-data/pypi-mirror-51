import os

import click

from developers_chamber.scripts import cli
from developers_chamber.version_utils import bump_to_next_version as bump_to_next_version_func
from developers_chamber.version_utils import get_next_version, get_version
from developers_chamber.types import EnumType, ReleaseType


default_version_files = os.environ.get('VERSION_FILES', 'version.json').split(',')


@cli.command()
@click.option('--release_type', help='release type', type=EnumType(ReleaseType), required=True)
@click.option('--build_hash',  help='hash of the build', type=str)
@click.option('--file',  help='path to the version file', type=str, default=default_version_files, required=True,
              multiple=True)
def version_bump_to_next(release_type, build_hash, file):
    """
    Bump JSON file (or files) version number
    """
    click.echo(bump_to_next_version_func(release_type, build_hash, file))


@cli.command()
@click.option('--file', help='path to the version file', type=str, default=default_version_files[0], required=True)
def version_print(file):
    """
    Return current project version according to version JSON file
    """
    click.echo(get_version(file))


@cli.command()
@click.option('--release_type', help='release type', type=EnumType(ReleaseType), required=True)
@click.option('--build_hash',  help='hash of the build', type=str)
@click.option('--file',  help='path to the version file', type=str, default=default_version_files[0], required=True)
def version_print_next(release_type, build_hash, file):
    """
    Return next version according to input release type, build hash and version JSON file
    """
    click.echo(get_next_version(release_type, build_hash, file))
