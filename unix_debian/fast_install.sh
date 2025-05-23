install_package() {
    PACKAGE=$1
    if ! dpkg -s "$PACKAGE" &> /dev/null; then
        echo "🔄 Installing package $PACKAGE..."
        sudo apt-get -y install "$PACKAGE"
        if [ $? -ne 0 ]; then
            echo "❌ Error: $PACKAGE installation failed"
            exit 1
        fi
        echo "✔️ $PACKAGE installed successfully."
    else
        echo "✔️ $PACKAGE is already installed."
    fi
}

# Function to install a Python package using pip3
install_python_package() {
    PACKAGE=$1
    # Check if pip3 is installed
    if ! command -v pip3 &> /dev/null; then
        echo "⚠️ pip3 is not installed. Installing pip3..."
        install_package python3-pip
        if [ $? -ne 0 ]; then
            echo "❌ Error: pip3 installation failed. Cannot install Python package."
            exit 1
        fi
    fi

    if ! python3 -c "import $PACKAGE" &> /dev/null; then
        echo "🔄 Installing Python package $PACKAGE..."
        sudo pip3 install "$PACKAGE" --break-system-packages
        if [ $? -ne 0 ]; then
            echo "❌ Error: $PACKAGE installation failed"
            exit 1
        fi
        echo "✔️ $PACKAGE installed successfully."
    else
        echo "✔️ $PACKAGE is already installed."
    fi
}