import pika

def callback(ch, method, properties, body):
    print(f"STAT: {body.decode()}")

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='colorStatistics')
channel.basic_consume(queue='colorStatistics', on_message_callback=callback, auto_ack=True)

print('Waiting for stats...')
channel.start_consuming()
