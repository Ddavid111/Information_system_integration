import pika
import random

def callback(ch, method, properties, body):
    if random.randint(1, 10) <= 3:
        print(f"RED rollback (send to DLQ): {body.decode()}")
        ch.basic_publish(exchange='',
                         routing_key='DLQ',
                         body=body)
    else:
        callback.processed += 1
        print(f"Processed RED: {body.decode()}")
        if callback.processed % 10 == 0:
            ch.basic_publish(exchange='',
                             routing_key='colorStatistics',
                             body=f"10 'RED' messages has been processed.".encode())

callback.processed = 0

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='colorExchange', exchange_type='direct')
channel.queue_declare(queue='RED')
channel.queue_bind(exchange='colorExchange', queue='RED', routing_key='RED')

channel.queue_declare(queue='colorStatistics')
channel.queue_declare(queue='DLQ')

channel.basic_consume(queue='RED', on_message_callback=callback, auto_ack=True)

print('Waiting for RED messages...')
channel.start_consuming()
