import json
from django.shortcuts import render
from django.core import serializers
from apps.serializers import PostSerializer

from rest_framework import viewsets
from rest_framework.response import Response

from .models import Post
from core.producer import publish

# Create your views here.

def post_list(request):
    posts = Post.objects.all()
    data = serializers.serialize('json', 
                                 posts)
    print(data)
    publish('post_list', data)
    return render(request, 'post/post_list.html', {'posts': posts})


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer=serializer)
        print(serializer.data)
        publish('create_post', json.dumps(serializer.data))
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save()
        
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, 
                                           data=request.data,
                                           )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        publish('update_post', json.dumps(serializer.data))
        return Response(serializer.data)
    
    def perform_update(self, serializer):
        serializer.save()
        
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        data = self.serializer_class(instance)
        print(data.data)
        self.perform_destroy(instance)
        publish('delete_post', json.dumps(data.data))
        return Response(data=data.data)
    