from rest_framework import serializers

from apps.models import Comment, Post


class CommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment
        fields = ('id', 'content', 'author', 'post_id')
        
        
class PostSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Post 
        fields = '__all__'
        
        
         