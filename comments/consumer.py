import json
import os
import pika
import logging
os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'

import django
django.setup()

from apps.serializers import PostSerializer
from  apps.models import Post   


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)
channel = connection.channel()
channel.queue_declare(queue="post")

def callback(ch, method, properties, body):
    print("Recieved in post")
    data = json.loads(body)
    if properties.content_type == 'create_post':
        print(data) 
        try:
            serializer = PostSerializer(data={
                'id': data["id"],
                'title': data["title"],
                'text': data["text"],
                'author': data["author"]
            })
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except:
            print("error")
            
    if properties.content_type == 'update_post':
        print(data) 
        try:
            post = Post.objects.get(id=data["id"])
            serializer = PostSerializer(
                instance=post,
                data={
                    'title': data["title"],
                    'text': data["text"],
                    'author': data["author"]
                })
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except:
            print("error")
        
    if properties.content_type == 'delete_post':
        post = Post.objects.get(id=data["id"])
        try:   
            post.delete()
        except :
            print("error")
        
        
    
channel.basic_consume(queue='post', on_message_callback=callback, auto_ack=True)

print('Started consuming')
channel.start_consuming()
channel.close()
