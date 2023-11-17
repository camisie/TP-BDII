#!/usr/bin/env bash
#
# HOW TO: Source this file! In your shell do:
#
# source ./activate_environment.sh
# 
# And that's it, the environment will be activated

VENV=".venv"

# Move to script dir to avoid Bash gotchas
SCRIPT_DIR=$(dirname "${BASH_SOURCE[0]}")
if ! pushd "${SCRIPT_DIR}" &> /dev/null; then
    echo "Woops! Could not pushd to script directory: '${SCRIPT_DIR}'"
    return 2
fi

# Verify Python is installed, and its version
PYTHON_VERSION="$(python --version | awk '{print $2}')"
if [ -z "$PYTHON_VERSION" ]; then
    echo "Python not found. Aborting"
    return 1
elif [[ "$(echo "${PYTHON_VERSION}" | awk -F '.' '{print $1}')" != "3" ]] || \
    [[ "$(echo "${PYTHON_VERSION}" | awk -F '.' '{print $2}')" -lt "8" ]]; then
    echo "At least Python 3.8 is required, but found ${PYTHON_VERSION}. Aborting"
    return 1
fi

# Create env if it does not exists
if [ ! -d "${VENV}" ]; then
    python3 -m venv "${VENV}"
    pip install -r "./requirements.txt"
fi

# Source env
if [ -d "${VENV}" ]; then
    source "${PWD}/${VENV}/bin/activate"
fi

# Move out of script dir
if ! popd &> /dev/null; then
    echo "Woops! Could not popd from script directory: '${SCRIPT_DIR}'"
    return 2
fi
