# Function to check if a command exists
command_exists() {
    COMMAND=$1
    if command -v "$COMMAND" &> /dev/null; then
        echo "✔️ Command '$COMMAND' exists."
        return 0 # True
    else
        echo "❌ Command '$COMMAND' does not exist."
        return 1 # False
    fi
}