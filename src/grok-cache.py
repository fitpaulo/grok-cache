#!/usr/bin/env python3

import tomli  # For parsing TOML (Python 3.11+)
import tomli_w  # For writing TOML
import pyperclip
import click
import os

cache_rel_path = "../cache/cache.toml"
cache_file_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), cache_rel_path
)


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """Grok Cache CLI: Manage cache statements for Grok interactions.

    Commands:
      copy <section> <key>  Copy a cache statement to clipboard
      list                  List all cache sections and keys
      add <section> <key>   Add or update a cache statement
    """
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@cli.command()
@click.argument("section")
@click.argument("key")
def copy(section, key):
    """Copy a cache statement to clipboard."""
    with open(cache_file_path, "rb") as f:
        data = tomli.load(f)
    try:
        prompt = data[section][key].strip()
        pyperclip.copy(prompt)
        click.echo(f"Copied '{key}' from '{section}' to clipboard!")
    except KeyError:
        click.echo(f"No '{key}' found in '{section}'.")


@cli.command()
def list():
    """List all cache statements by section."""
    with open(cache_file_path, "rb") as f:
        data = tomli.load(f)
    for section, items in data.items():
        click.echo(f"\n[{section}]")
        for key in items:
            click.echo(f"  {key}")


@cli.command()
@click.argument("section")
@click.argument("key")
def add(section, key):
    """Add or update a cache statement in the TOML file."""
    # Load existing data or start fresh
    if os.path.exists(cache_file_path):
        with open(cache_file_path, "rb") as f:
            data = tomli.load(f)
    else:
        data = {}

    # Prompt user for the cache statement
    prompt = click.prompt(f"Enter cache statement for [{section}].{key}", type=str)

    # Add or update section and key
    if section not in data:
        data[section] = {}
    data[section][key] = prompt

    # Write back to file
    with open(cache_file_path, "wb") as f:
        tomli_w.dump(data, f)
    click.echo(f"Added/Updated '{key}' in '{section}'.")


@cli.command()
@click.argument("section")
@click.argument("key")
def delete(section, key):
    """Delete a cache statement from the TOML file."""
    if not os.path.exists(cache_file_path):
        click.echo("No cache file found.")
        return

    with open(cache_file_path, "rb") as f:
        data = tomli.load(f)

    try:
        del data[section][key]
        if not data[section]:  # If section’s empty, remove it
            del data[section]
        with open(cache_file_path, "wb") as f:
            tomli_w.dump(data, f)
        click.echo(f"Deleted '{key}' from '{section}'.")
    except KeyError:
        click.echo(f"No '{key}' found in '{section}'.")


if __name__ == "__main__":
    cli()
