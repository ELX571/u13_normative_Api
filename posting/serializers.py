from rest_framework import serializers
from posting.models import Post

class PostSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['from_user']

    def validate(self, data):
        title = data.get('title')
        content = data.get('content')

        if len(title) == 0:
            raise serializers.ValidationError("Title wrong (title cannot be blank)")
        elif len(content) < 10:
            raise serializers.ValidationError("Content wrong (content cannot be less than 10)")
        return data

class PostListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Post
        fields = '__all__'


class PostUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Post
        fields = '__all__'


