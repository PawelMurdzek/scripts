# Function to uninstall a Debian package
uninstall_package() {
    PACKAGE=$1
    if dpkg -s "$PACKAGE" &> /dev/null; then
        echo "🔄 Uninstalling package $PACKAGE..."
        sudo apt-get -y remove "$PACKAGE"
        if [ $? -ne 0 ]; then
            echo "❌ Error: $PACKAGE uninstallation failed"
            exit 1
        fi
        echo "✔️ $PACKAGE uninstalled successfully."
    else
        echo "✔️ $PACKAGE is not installed."
    fi
}

# Function to uninstall a Python package using pip3
uninstall_python_package() {
    PACKAGE=$1
    # Check if pip3 is installed
    if ! command -v pip3 &> /dev/null; then
        echo "❌ Error: pip3 is not installed. Cannot uninstall Python package."
        exit 1
    fi

    # Check if the Python package is installed by trying to import it
    if python3 -c "import $PACKAGE" &> /dev/null; then
        echo "🔄 Uninstalling Python package $PACKAGE..."
        sudo pip3 uninstall -y "$PACKAGE" --break-system-packages
        if [ $? -ne 0 ]; then
            echo "❌ Error: $PACKAGE uninstallation failed"
            exit 1
        fi
        echo "✔️ $PACKAGE uninstalled successfully."
    else
        echo "✔️ Python package $PACKAGE is not installed."
    fi
}