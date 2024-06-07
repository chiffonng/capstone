#!/bin/bash

download_zipped_file() {
    local url=$1
    local output=$2

    # Check if wget is available
    if command -v wget >/dev/null 2>&1; then
        echo "⬇️ Downloading $url using wget..."
        wget --no-check-certificate --show-progress -O "$output" "$url"
    elif command -v curl >/dev/null 2>&1; then
        echo "⬇️ Downloading $url using curl..."
        curl -k -L -o "$output" "$url"
    else
        echo "❌ Error: Neither wget nor curl is available for downloading. Please install either one and try again, or download the file manually from $url."
        exit 1
    fi
}
# Get Nutch as web crawler https://www.apache.org/dyn/closer.cgi/nutch/
download_nutch() {
    local version=$1
    local nutch_parent_dir=$2
    cd "$nutch_parent_dir" || exit 1 
    download_zipped_file "https://www.apache.org/dyn/closer.cgi/nutch/$version/apache-nutch-$version-bin.zip" "nutch.zip"
    mv apache-nutch-$version-bin nutch
    rm -f nutch.zip
    cd ..
}

# Verify installation
verify_nutch() {
    if [ -d "bin/nutch" ]; then
        echo "✅ Nutch is installed successfully."
    else
        echo "❌ Error: Nutch installation failed."
        exit 1
    fi
}

# Main function
main() {
    local version=$1
    local nutch_parent_dir="nutch"
    download_nutch "$version" "$nutch_parent_dir"
    verify_nutch
}

# Run the main function with the provided version
main "$1"