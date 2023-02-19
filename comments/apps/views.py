import json
from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.response import Response

from apps.models import Comment, Post
from apps.serializers import CommentSerializer, PostSerializer
from core.producer import publish

# Create your views here.


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
   
    
   
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    
    def create(self, request, *args, **kwargs):
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(self.kwargs)
        self.perform_create(serializer=serializer)
        publish('comment_created', json.dumps(serializer.data))
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = CommentSerializer(instance=instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        publish('comment_updated', json.dumps(serializer.data))
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        data = self.serializer_class(instance)
        print(data.data)
        self.perform_destroy(instance)
        publish('comment_deleted', json.dumps(data.data))
        return Response(data=data.data)
   