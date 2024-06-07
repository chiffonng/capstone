# Java base image https://hub.docker.com/_/amazoncorretto/tags
FROM amazoncorretto:8u412-al2023-jre

# Set the working directory
WORKDIR /workspace

# Variables
ENV NUTCH_VERSION 1.20

# Copy the scripts
COPY ../scripts ./scripts

# Download and install Nutch
RUN bash scripts/install-nutch.sh "$NUTCH_VERSION"

# Expose the port Nutch server runs on
EXPOSE 8080

# Run Nutch
CMD ["nutch/bin/nutch", "webapp"]