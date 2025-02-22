# Grok-Cache CLI

A simple command-line tool to manage cache statements for interactions with Grok (xAI). Store, retrieve, and delete prompts in a TOML file—perfect for picking up where you left off.

## Features
- **Copy**: Grab a cached prompt to your clipboard.
- **List**: View all sections and keys in the cache.
- **Add**: Save or update a prompt under a section and key.
- **Delete**: Remove a specific prompt (alias: `del`).

## Installation
1. Clone the repo:
   ```bash
   git clone <your-repo-url>
   cd grok-cache
2. Install dependencies:
   pip install tomli tomli-w pyperclip click
3. Make it executalbe
   chmod +x src/grok-cache.py
4. Link it on your path
   ln -s $PWD/src/grok-cache.py $HOME/.local/bin

## Usage
grok-cache.py <command> [options] [args]

## Commands
 * `-c, copy <section> <key>`: Copy a prompt to clipboard.
