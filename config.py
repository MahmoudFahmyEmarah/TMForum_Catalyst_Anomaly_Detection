# Kafka Configuration
KAFKA_BROKER_URL = "kafka.arcturusdev.svc.cluster.local:9092"
KAFKA_CONSUMER_CONFIG = {
    "security.protocol": "SASL_PLAINTEXT",
    "sasl.mechanism": "SCRAM-SHA-256",
    "sasl.jaas.config": 'org.apache.kafka.common.security.scram.ScramLoginModule required username="user1" password="PD17aJYqay";'
}

# API Configuration
API_BASE_URL = "https://arcturus-api.dev.apps.qeema.io/api/product/"
