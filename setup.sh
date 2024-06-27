#! /bin/bash

# Set up variables
ENV_NAME="whatsappLLM"
REQ_FILE="requirements.txt"
CONFIG_FILE="config.py"

# Function to print messages
function print_message() {
    echo ""
    echo "==================================="
    echo $1
    echo "==================================="
    echo ""
}

# Function to check if conda environment exists
function check_conda_env() {
    conda env list | grep $ENV_NAME >/dev/null 2>&1
}

# Step 1: Check if conda environment exists
print_message "Checking if conda environment already exists..."
if check_conda_env; then
    print_message "Conda environment '$ENV_NAME' already exists. Skipping creation."
else
    print_message "Creating conda environment..."
    conda create --name $ENV_NAME python=3.8 -y
fi

# Step 2: Activate conda environment
print_message "Activating conda environment..."
source $(conda info --base)/etc/profile.d/conda.sh
conda activate $ENV_NAME

# Step 3: Install dependencies
print_message "Installing dependencies..."
pip install --upgrade pip
pip install -r $REQ_FILE

# Step 4: Create config.py if it doesn't exist
if [ ! -f $CONFIG_FILE ]; then
    print_message "Creating config.py file..."
    echo "cohere_api_key = 'your_cohere_api_key'" > $CONFIG_FILE
    echo "Please update config.py with your actual Cohere API key."
else
    print_message "config.py already exists. Skipping creation."
fi

print_message "Setup complete. Should be inside conda environment: $ENV_NAME" 
