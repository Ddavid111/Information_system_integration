import pika

def callback(ch, method, properties, body):
    print(f"DLQ received: {body.decode()}")

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='DLQ')
channel.basic_consume(queue='DLQ', on_message_callback=callback, auto_ack=True)

print('Waiting for DLQ messages...')
channel.start_consuming()
