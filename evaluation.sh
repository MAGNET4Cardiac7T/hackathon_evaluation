#!/bin/sh

# Check if both repository URL and group name are provided
if [ -z "$1" ]; then
    echo "Usage: $0 <repository_url> <group_name>"
    exit 1
fi
REPO_URL=$1

# Check if a group name is provided
if [ -z "$2" ]; then
    # set default group name
    GROUP_NAME="default_group"
    echo "Usage: $0 <repository_url> <group_name>"
    echo "No group name provided. Using default group name: $GROUP_NAME"
else
    GROUP_NAME=$2
    echo "Using provided group name: $GROUP_NAME"
fi

# Remove the /code directory if it exists and recreate it
rm -rf code
mkdir code

# Clone the repository into /code
git clone "$REPO_URL" code
if [ $? -ne 0 ]; then
    echo "Failed to clone repository."
    exit 1
fi

# Extract the repository name from the URL
REPO_NAME=$(basename "$REPO_URL" .git)

# Enter the /code directory
if [ -d "code" ]; then
    cd code || exit
    echo "Entered repository directory: code"
else
    echo "code directory not found."
    exit 1
fi

# Check if requirements.txt exists and set up a Python virtual environment
if [ -f "requirements.txt" ]; then
    echo "Setting up Python virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "Failed to create virtual environment."
        exit 1
    fi

    # Activate the virtual environment
    . venv/bin/activate

    # Install dependencies
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "Failed to install dependencies."
        deactivate
        exit 1
    fi

    echo "Python environment setup complete."
else
    echo "No requirements.txt found. Exiting."
    exit 1
fi

cd ..

# Check if data_list.txt exists
if [ ! -f "data_list.txt" ]; then
    echo "data_list.txt not found. Exiting."
    exit 1
fi

# Check if cost_list.txt exists
if [ ! -f "cost_list.txt" ]; then
    echo "cost_list.txt not found. Exiting."
    exit 1
fi

# Read cost functions from cost_list.txt
COST_FUNCTIONS=$(cat cost_list.txt)
SIMULATIONS=$(cat data_list.txt)

# Read each line from data_list.txt and iterate over cost functions
for simulation_file in $SIMULATIONS; do
    for cost_function in $COST_FUNCTIONS; do
        echo "Processing simulation file: $simulation_file with cost function: $cost_function"
        timeout -v -k 10 300 python run_optimization.py -f "$simulation_file" -c "$cost_function"
        python evaluate.py -f "$simulation_file" -c "$cost_function" -g "$GROUP_NAME"
        if [ $? -ne 0 ]; then
            echo "Failed to process simulation file: $simulation_file with cost function: $cost_function"
            exit 1
        fi
        if [ -f "best_coil_config.json" ]; then
            rm best_coil_config.json
        fi
    done
done

