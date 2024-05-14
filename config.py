# Kafka Configuration
#KAFKA_BROKER_URL = "kafka.arcturusdev.svc.cluster.local:9092"
KAFKA_BROKER_URL = "65.109.43.234:31760"
KAFKA_CONSUMER_TOPIC ='order.completed.topic'
KAFKA_PRODUCER_TOPIC ='order.complaint.topic'
KAFKA_CONSUMER_CONFIG = {
    'security_protocol':'SASL_PLAINTEXT',
    'sasl_mechanism':'PLAIN',
    'sasl_plain_username':'user1',
    'sasl_plain_password':'PD17aJYqay'
}

# API Configuration
API_BASE_URL = "https://arcturus-api.dev.apps.qeema.io/api/product/"
