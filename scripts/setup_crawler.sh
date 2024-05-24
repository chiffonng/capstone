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
cd crawler
download_zipped_file https://dlcdn.apache.org/nutch/1.20/apache-nutch-1.20-bin.zip nutch.zip 
unzip -n nutch.zip
mv apache-nutch-1.20-bin nutch
rm nutch.zip

# Get Solr as search engine https://www.apache.org/dyn/closer.lua/lucene/solr/8.11.1
# Make sure the following is inside crawler directory
download_zipped_file https://www.apache.org/dyn/closer.lua/solr/solr/9.6.0/solr-9.6.0.tgz?action=download solr.tgz
tar -xzf solr.tgz
mv solr-9.6.0 solr
rm solr.tgz


# Set up Nutch
cd nutch

# Set up Solr
