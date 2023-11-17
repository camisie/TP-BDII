#!/usr/bin/env bash
#

# Move to script dir to avoid Bash gotchas
SCRIPT_DIR=$(dirname "${BASH_SOURCE[0]}")
if ! pushd "${SCRIPT_DIR}" &> /dev/null; then
    echo "Woops! Could not pushd to script directory: '${SCRIPT_DIR}'"
    return 2
fi

ENV_FILE="./activate_environment.sh"
if [ ! -f "$ENV_FILE" ]; then
    echo "Environment file not found. Aborting"
    exit 1
fi

source "${ENV_FILE}"

API_DB=""
echo "Select the database:"
options=("MongoDB" "PostgreSQL")

select opt in "${options[@]}"
do
    case ${opt,,} in
        "mongodb")
            API_DB="mongodb"
            break
            ;;
        "postgresql")
            API_DB="postgresql"
            break
            ;;
        *) echo "Invalid option";;
    esac
done

export API_DB

# Launch server
uvicorn main:app --reload

# Move out of script dir
if ! popd &> /dev/null; then
    echo "Woops! Could not popd from script directory: '${SCRIPT_DIR}'"
    return 2
fi
