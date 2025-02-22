#!/usr/bin/env python3
import tomli
import tomli_w
import pyperclip
import click
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
cache_rel_path = "../cache/cache.toml"
cache_file_path = os.path.join(script_dir, cache_rel_path)


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """Grok Cache CLI: Manage cache statements for Grok interactions.

    Commands:
      copy (-c) <section> <key>  Copy a cache statement to clipboard
      list (-l)                  List all cache sections and keys
      add (-a) <section> <key>   Add or update a cache statement
      delete (-d) <section> <key>  Delete a cache statement (alias: del)
    """
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@cli.command(name="copy", short_help="Copy a cache statement")
@click.option("-c", is_flag=True, help="Copy a cache statement (alias)")
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


@cli.command(name="list", short_help="List all cache statements")
@click.option("-l", is_flag=True, help="List all cache statements (alias)")
def list_cmd():
    """List all cache statements by section."""
    with open(cache_file_path, "rb") as f:
        data = tomli.load(f)
    for section, items in data.items():
        click.echo(f"\n[{section}]")
        for key in items:
            click.echo(f"  {key}")


@cli.command(name="add", short_help="Add or update a cache statement")
@click.option("-a", is_flag=True, help="Add or update a cache statement (alias)")
@click.argument("section")
@click.argument("key")
def add(section, key):
    """Add or update a cache statement in the TOML file."""
    if os.path.exists(cache_file_path):
        with open(cache_file_path, "rb") as f:
            data = tomli.load(f)
    else:
        data = {}

    prompt = click.prompt(f"Enter cache statement for [{section}].{key}", type=str)
    if section not in data:
        data[section] = {}
    data[section][key] = prompt
    with open(cache_file_path, "wb") as f:
        tomli_w.dump(data, f)
    click.echo(f"Added/Updated '{key}' in '{section}'.")


@cli.command(name="delete", short_help="Delete a cache statement", aliases=["del"])
@click.option("-d", is_flag=True, help="Delete a cache statement (alias)")
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
        if not data[section]:
            del data[section]
        with open(cache_file_path, "wb") as f:
            tomli_w.dump(data, f)
        click.echo(f"Deleted '{key}' from '{section}'.")
    except KeyError:
        click.echo(f"No '{key}' found in '{section}'.")


if __name__ == "__main__":
    cli()
