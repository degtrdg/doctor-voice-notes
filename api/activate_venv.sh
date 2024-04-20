#!/bin/bash
# Script to activate a Python virtual environment in the .venv directory

# Folder to put venv in
venv_dir="./.venv"

# Check if the virtual environment exists
if [ -d "$venv_dir" ]; then
	# Check if the virtual environment is already activated
	if [ -z "$VIRTUAL_ENV" ]; then
		# Activate the virtual environment
		source "$venv_dir/bin/activate"

		# Check if the activation was successful
		if [ -n "$VIRTUAL_ENV" ]; then
			echo "Activated venv"
			echo "Deactivate the virtual environment with 'deactivate'"
		else
			echo "Failed to activate venv in '$venv_dir'"
		fi
	else
		echo "A virtual environment is already activated ('$VIRTUAL_ENV')"
	fi
else
	echo "Virtual environment in '$venv_dir' not found"
fi
