import pika
import random
import time

def wait_for_rabbitmq():
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
            return connection
        except pika.exceptions.AMQPConnectionError:
            print("RabbitMQ not ready, waiting...")
            time.sleep(2)

connection = wait_for_rabbitmq()
channel = connection.channel()

channel.exchange_declare(exchange='colorExchange', exchange_type='direct', durable=True)

colors = ['RED', 'GREEN', 'BLUE']

while True:
    color = random.choice(colors)
    channel.basic_publish(exchange='colorExchange',
                          routing_key=color,
                          body=f"Color message: {color}")
    print(f"Sent: {color}")
    time.sleep(1)
