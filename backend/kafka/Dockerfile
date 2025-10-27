FROM apache/kafka-native

# Copy the setup script with executable permissions
COPY --chmod=+x kafka-setup.sh /kafka-setup.sh

# Set the entrypoint
ENTRYPOINT ["/kafka-setup.sh"]
