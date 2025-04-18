import pika
import random
import time

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='colorExchange', exchange_type='direct')

colors = ['RED', 'GREEN', 'BLUE']

while True:
    color = random.choice(colors)
    channel.basic_publish(exchange='colorExchange',
                          routing_key=color,
                          body=f"Color message: {color}")
    print(f"Sent: {color}")
    time.sleep(1)
