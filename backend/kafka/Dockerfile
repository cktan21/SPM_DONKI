FROM confluentinc/cp-kafka:7.4.0

# Copy the setup script
COPY kafka-setup.sh /usr/bin/kafka-setup.sh
RUN chmod +x /usr/bin/kafka-setup.sh

# Set the entrypoint
ENTRYPOINT ["/usr/bin/kafka-setup.sh"]
