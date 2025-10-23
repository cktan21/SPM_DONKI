FROM confluentinc/cp-kafka:7.4.0

# Copy the setup script with executable permissions
COPY --chmod=755 kafka-setup.sh /usr/bin/kafka-setup.sh

# Set the entrypoint
ENTRYPOINT ["/usr/bin/kafka-setup.sh"]
