#!/bin/bash
# Script to create a Python 3 virtual environment and install packages from requirements.txt

# Kinda hacky way of checking if Python 3 is installed
if ! command -v python3 &>/dev/null; then
	echo "Python 3 is not installed. Might be python3 installation or symlink thing"
	exit 1
fi

# Folder to put venv in
venv_name="./.venv"

# Check if venv already exists
if [ -d "$venv_name" ]; then
	echo "Virtual environment '$venv_name' already exists. Skipping creation"
else
	# Create venv
	python3.11 -m venv "$venv_name"
	echo "Virtual environment '$venv_name' created"
fi

# Activate venv
source "$venv_name/bin/activate"
echo "Activated virtual environment '$venv_name'"

# Install packages from requirements.txt
if [ -f "./requirements.txt" ]; then
	pip install -r ./requirements.txt
	echo "Installed packages from requirements.txt"
else
	echo "requirements.txt not found. No packages were installed"
fi
