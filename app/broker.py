from faststream.rabbit import RabbitBroker, RabbitQueue, RabbitExchange, ExchangeType

RABBITMQ_URL = "amqp://guest:guest@localhost:5672/"

broker = RabbitBroker(RABBITMQ_URL)

payments_exchange = RabbitExchange("payments.exchange", type=ExchangeType.DIRECT)
payments_queue = RabbitQueue("payments.new", durable=True, routing_key="payments.new")
dlq_queue = RabbitQueue("payments.dlq", durable=True)