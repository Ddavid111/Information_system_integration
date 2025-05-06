import pika
import time

def wait_for_rabbitmq():
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
            return connection
        except pika.exceptions.AMQPConnectionError:
            print("RabbitMQ not ready, waiting...")
            time.sleep(2)

def callback(ch, method, properties, body):
    print(f"STAT: {body.decode()}")

connection = wait_for_rabbitmq()
channel = connection.channel()

channel.queue_declare(queue='colorStatistics', durable=True)
channel.basic_consume(queue='colorStatistics', on_message_callback=callback, auto_ack=True)

print('Waiting for stats...')
channel.start_consuming()
