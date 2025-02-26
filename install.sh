#!/bin/bash

# Define directories
CONFIG_DIR="$HOME/.config/grok-cache"
CACHE_DIR="$HOME/.local/share/grok-cache"
BIN_DIR="$HOME/.local/bin"
REPO_DIR="$(realpath "$(dirname "$0")")"  # Root of git repo
REPO_ALIASES="$REPO_DIR/config/aliases.ini"

# Check if aliases.ini exists in repo
if [ ! -f "$REPO_ALIASES" ]; then
    echo "Error: $REPO_ALIASES not found in repo!"
    exit 1
fi

# Create directories
mkdir -p "$CONFIG_DIR" || { echo "Failed to create $CONFIG_DIR"; exit 1; }
mkdir -p "$CACHE_DIR" || { echo "Failed to create $CACHE_DIR"; exit 1; }

# Copy aliases.ini from repo if it doesn’t exist
ALIASES_FILE="$CONFIG_DIR/aliases.ini"
if [ ! -f "$ALIASES_FILE" ]; then
    cp "$REPO_ALIASES" "$ALIASES_FILE" && echo "Copied $REPO_ALIASES to $ALIASES_FILE"
else
    echo "$ALIASES_FILE already exists—skipping copy."
fi

# Symlink grok-cache.py to ~/.local/bin
SCRIPT_PATH="$REPO_DIR/src/grok-cache.py"
SYMLINK_PATH="$BIN_DIR/grok-cache"

if [ ! -d "$BIN_DIR" ]; then
    mkdir -p "$BIN_DIR" || { echo "Failed to create $BIN_DIR"; exit 1; }
fi

if [ ! -L "$SYMLINK_PATH" ]; then
    ln -s "$SCRIPT_PATH" "$SYMLINK_PATH" && echo "Symlinked $SCRIPT_PATH to $SYMLINK_PATH"
else
    echo "$SYMLINK_PATH already exists—skipping symlink."
fi

# Print PATH update instructions
echo
echo "=============================================================="
echo "Add ~/.local/bin to your shell's PATH to run 'grok-cache' from anywhere!"
echo "Copy and run one of these command pairs based on your shell:"
echo
echo "For Bash (~/.bashrc):"
echo "  echo 'export PATH=\"\$PATH:$HOME/.local/bin\"' >> ~/.bashrc"
echo "  . ~/.bashrc"
echo
echo "For Zsh (~/.zshrc):"
echo "  echo 'export PATH=\"\$PATH:$HOME/.local/bin\"' >> ~/.zshrc"
echo "  . ~/.zshrc"
echo
echo "For Fish (~/.config/fish/config.fish):"
echo "  echo 'fish_add_path $HOME/.local/bin' >> ~/.config/fish/config.fish"
echo "  source ~/.config/fish/config.fish"
echo "=============================================================="
echo
echo "Install complete! Run 'grok-cache --help' to get started (after updating PATH)."
