import json
import os
import pika


os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'
import django

django.setup()

from apps.serializers import CommentSerializer, PostSerializer
from apps.models import Comment


connexion = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)

canal = connexion.channel()

canal.queue_declare('comment')

def callback(ch, method, properties, body):
    data = json.loads(body)
    properties = properties.content_type
    print(properties)
    
    if properties == 'comment_created':
        print(data)
        serializer = CommentSerializer(data={
            'id': data['id'],
            'content': data['content'],
            'author': data['author'],
            'post_id': data['post_id'],
        })
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
    if properties == 'comment_updated':
        print(data)
        try:
            instance = Comment.objects.get(id=data['id'])
            serializer = CommentSerializer(
                instance=instance,
                data={
                    'id': data['id'],
                    'content': data['content'],
                    'author': data['author'],
                    'post_id': data['post_id'],
            })
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except:
            print("Error")
          
    if properties == 'comment_deleted':
        comment = Comment.objects.get(id=data["id"])
        try:   
            comment.delete()
        except :
            print("error")  
            
            
canal.basic_consume(queue='comment', on_message_callback=callback, auto_ack=True)
print("Starting consuming")

canal.start_consuming()