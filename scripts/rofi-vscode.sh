#!/bin/bash

# Set the path to your VSCode workspaces folder
WORKSPACES_DIR="$HOME/Coding/code_workspace/"

# Get the list of workspace files in the folder
WORKSPACES=$(find "$WORKSPACES_DIR" -name "*.code-workspace" -exec basename {} \;)

# Use Rofi to display the list and get user input
SELECTED_WORKSPACE=$(echo "$WORKSPACES" | rofi -dmenu -i -p "Select a workspace:")

# Check if a workspace was selected
if [ -n "$SELECTED_WORKSPACE" ]; then
	# Open the selected workspace in VSCode
	code "$WORKSPACES_DIR/$SELECTED_WORKSPACE"
fi
