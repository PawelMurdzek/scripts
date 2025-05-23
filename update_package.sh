# Function to update a Debian package (or all packages)
update_package() {
    PACKAGE=$1
    if [ -z "$PACKAGE" ]; then
        echo "🔄 Updating all installed packages..."
        sudo apt-get update && sudo apt-get -y upgrade
        if [ $? -ne 0 ]; then
            echo "❌ Error: All packages update failed"
            exit 1
        fi
        echo "✔️ All packages updated successfully."
    else
        echo "🔄 Updating package $PACKAGE..."
        sudo apt-get -y install --only-upgrade "$PACKAGE"
        if [ $? -ne 0 ]; then
            echo "❌ Error: $PACKAGE update failed"
            exit 1
        fi
        echo "✔️ $PACKAGE updated successfully."
    fi
}