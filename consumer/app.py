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

def callback(ch, method, properties, body, color):
    if random.randint(1, 10) <= 3:
        print(f"{color} rollback (send to DLQ): {body.decode()}")
        ch.basic_publish(exchange='',
                         routing_key='DLQ',
                         body=body)
    else:
        callback.processed[color] += 1
        print(f"Processed {color}: {body.decode()}")
        if callback.processed[color] % 10 == 0:
            ch.basic_publish(exchange='',
                             routing_key='colorStatistics',
                             body=f"10 '{color}' messages have been processed.".encode())

callback.processed = {
    'RED': 0,
    'GREEN': 0,
    'BLUE': 0
}

colors = ['RED', 'GREEN', 'BLUE']

connection = wait_for_rabbitmq()
channel = connection.channel()

channel.exchange_declare(exchange='colorExchange', exchange_type='direct', durable=True)

for color in colors:
    channel.queue_declare(queue=color, durable=True)
    channel.queue_bind(exchange='colorExchange', queue=color, routing_key=color)

channel.queue_declare(queue='colorStatistics', durable=True)
channel.queue_declare(queue='DLQ', durable=True)

for color in colors:
    channel.basic_consume(queue=color, 
                          on_message_callback=lambda ch, method, properties, body, color=color: callback(ch, method, properties, body, color), 
                          auto_ack=True)

print('Waiting for color messages...')
channel.start_consuming()
