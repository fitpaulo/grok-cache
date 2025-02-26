#!/bin/bash

# Define directories
CONFIG_DIR="$HOME/.config/grok-cache"
CACHE_DIR="$HOME/.local/share/grok-cache"
BIN_DIR="$HOME/.local/bin"  # Changed to .local/bin

# Create directories
mkdir -p "$CONFIG_DIR" || { echo "Failed to create $CONFIG_DIR"; exit 1; }
mkdir -p "$CACHE_DIR" || { echo "Failed to create $CACHE_DIR"; exit 1; }

# Generate aliases.ini if it doesn’t exist
ALIASES_FILE="$CONFIG_DIR/aliases.ini"
if [ ! -f "$ALIASES_FILE" ]; then
    cat << EOF > "$ALIASES_FILE"
[aliases]
del = delete
EOF
    echo "Created $ALIASES_FILE with default aliases."
else
    echo "$ALIASES_FILE already exists—skipping creation."
fi

# Symlink grok-cache.py to ~/.local/bin
SCRIPT_PATH="$(realpath "$(dirname "$0")/src/grok-cache.py")"
SYMLINK_PATH="$BIN_DIR/grok-cache"

if [ ! -d "$BIN_DIR" ]; then
    mkdir -p "$BIN_DIR" || { echo "Failed to create $BIN_DIR"; exit 1; }
fi

if [ ! -L "$SYMLINK_PATH" ]; then
    ln -s "$SCRIPT_PATH" "$SYMLINK_PATH" && echo "Symlinked $SCRIPT_PATH to $SYMLINK_PATH"
else
    echo "$SYMLINK_PATH already exists—skipping symlink."
fi

echo "Install complete! Run 'grok-cache --help' to get started."
