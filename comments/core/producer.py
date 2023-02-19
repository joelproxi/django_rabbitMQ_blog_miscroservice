import os
import pika


connexion = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)
channel = connexion.channel()

def publish(method, body):
    print(body)
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', body=body, properties=properties, routing_key='comment')

