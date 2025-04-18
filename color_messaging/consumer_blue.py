import pika
import random

def callback(ch, method, properties, body):
    if random.randint(1, 10) <= 3:
        print(f"BLUE rollback (send to DLQ): {body.decode()}")
        ch.basic_publish(exchange='',
                         routing_key='DLQ',
                         body=body)
    else:
        callback.processed += 1
        print(f"Processed BLUE: {body.decode()}")
        if callback.processed % 10 == 0:
            ch.basic_publish(exchange='',
                             routing_key='colorStatistics',
                             body=f"10 'BLUE' messages has been processed.".encode())

callback.processed = 0

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='colorExchange', exchange_type='direct')
channel.queue_declare(queue='BLUE')
channel.queue_bind(exchange='colorExchange', queue='BLUE', routing_key='BLUE')

channel.queue_declare(queue='colorStatistics')
channel.queue_declare(queue='DLQ')

channel.basic_consume(queue='BLUE', on_message_callback=callback, auto_ack=True)

print('Waiting for BLUE messages...')
channel.start_consuming()
