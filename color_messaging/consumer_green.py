import pika
import random

def callback(ch, method, properties, body):
    if random.randint(1, 10) <= 3:
        print(f"GREEN rollback (send to DLQ): {body.decode()}")
        ch.basic_publish(exchange='',
                         routing_key='DLQ',
                         body=body)
    else:
        callback.processed += 1
        print(f"Processed GREEN: {body.decode()}")
        if callback.processed % 10 == 0:
            ch.basic_publish(exchange='',
                             routing_key='colorStatistics',
                             body=f"10 'GREEN' messages has been processed.".encode())

callback.processed = 0

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='colorExchange', exchange_type='direct', durable=True)

channel.queue_declare(queue='GREEN', durable=True)
channel.queue_bind(exchange='colorExchange', queue='GREEN', routing_key='GREEN')

channel.queue_declare(queue='colorStatistics', durable=True)
channel.queue_declare(queue='DLQ', durable=True)

channel.basic_consume(queue='GREEN', on_message_callback=callback, auto_ack=True)

print('Waiting for GREEN messages...')
channel.start_consuming()
