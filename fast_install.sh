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

install_python_package() {
    PACKAGE=$1
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