#!/usr/bin/env python3
import tomli
import tomli_w
import pyperclip
import click
import os
import configparser
import textwrap
from typing import Optional, List

# User config and data dirs (assumed to exist)
config_dir = os.path.expanduser("~/.config/grok-cache")
cache_dir = os.path.expanduser("~/.local/share/grok-cache")
aliases_file = os.path.join(config_dir, "aliases.ini")
cache_file_path = os.path.join(cache_dir, "cache.toml")


class AliasedGroup(click.MultiCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aliases = {}
        if os.path.exists(aliases_file):
            config = configparser.ConfigParser()
            config.read(aliases_file)
            if "aliases" in config:
                self.aliases = dict(config["aliases"])

    def list_commands(self, ctx: click.Context) -> List[str]:
        commands = ["copy", "list", "add", "delete"]
        alias_keys = [str(k) for k in self.aliases.keys()]
        commands.extend(alias_keys)
        return sorted(commands)

    def get_command(self, ctx: click.Context, cmd_name: str) -> Optional[click.Command]:
        cmd_name = self.aliases.get(cmd_name, cmd_name)

        def copy_callback(section, key, c=False):
            with open(cache_file_path, "rb") as f:
                data = tomli.load(f)
            try:
                prompt = data[section][key].strip()
                pyperclip.copy(prompt)
                click.echo(f"Copied '{key}' from '{section}' to clipboard!")
            except KeyError:
                click.echo(f"No '{key}' found in '{section}'.")

        def list_callback(l=False):
            if not os.path.exists(cache_file_path):
                click.echo("No cache file found.")
                return
            with open(cache_file_path, "rb") as f:
                data = tomli.load(f)
            for section, items in data.items():
                click.echo(f"\n[{section}]")
                for key, value in items.items():
                    if l:  # Verbose mode with -l
                        wrapped_value = textwrap.fill(
                            value,
                            width=80,
                            initial_indent="    ",
                            subsequent_indent="    ",
                        )
                        click.echo(f"  {key}:")
                        click.echo(wrapped_value)
                    else:  # Compact mode
                        click.echo(f"  {key}")

        def add_callback(section, key, a=False):
            if os.path.exists(cache_file_path):
                with open(cache_file_path, "rb") as f:
                    data = tomli.load(f)
            else:
                data = {}
            prompt = click.prompt(
                f"Enter cache statement for [{section}].{key}", type=str
            )
            if section not in data:
                data[section] = {}
            data[section][key] = prompt
            with open(cache_file_path, "wb") as f:
                tomli_w.dump(data, f)
            click.echo(f"Added/Updated '{key}' in '{section}'.")

        def delete_callback(section, key, d=False):
            if not os.path.exists(cache_file_path):
                click.echo("No cache file found.")
                return
            with open(cache_file_path, "rb") as f:
                data = tomli.load(f)
            try:
                del data[section][key]
                if not data[section]:
                    del data[section]
                with open(cache_file_path, "wb") as f:
                    tomli_w.dump(data, f)
                click.echo(f"Deleted '{key}' from '{section}'.")
            except KeyError:
                click.echo(f"No '{key}' found in '{section}'.")

        commands = {
            "copy": click.Command(
                name="copy",
                short_help="Copy a cache statement",
                callback=copy_callback,
                params=[
                    click.Option(
                        ["-c"], is_flag=True, help="Copy a cache statement (alias)"
                    ),
                    click.Argument(["section"]),
                    click.Argument(["key"]),
                ],
            ),
            "list": click.Command(
                name="list",
                short_help="List all cache statements",
                callback=list_callback,
                params=[
                    click.Option(
                        ["-l"], is_flag=True, help="Show verbose list with values"
                    ),
                ],
            ),
            "add": click.Command(
                name="add",
                short_help="Add or update a cache statement",
                callback=add_callback,
                params=[
                    click.Option(
                        ["-a"],
                        is_flag=True,
                        help="Add or update a cache statement (alias)",
                    ),
                    click.Argument(["section"]),
                    click.Argument(["key"]),
                ],
            ),
            "delete": click.Command(
                name="delete",
                short_help="Delete a cache statement",
                callback=delete_callback,
                params=[
                    click.Option(
                        ["-d"], is_flag=True, help="Delete a cache statement (alias)"
                    ),
                    click.Argument(["section"]),
                    click.Argument(["key"]),
                ],
            ),
        }

        return commands.get(cmd_name)


@click.command(cls=AliasedGroup, invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """Grok Cache CLI: Manage cache statements for Grok interactions."""
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


if __name__ == "__main__":
    cli()
