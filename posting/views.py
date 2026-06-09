from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from posting.models import Post
from posting.serializers import PostSerializer, PostListSerializer


# Create your views here.
def salomApiView(request):
    return JsonResponse({'message':'Hello World!'})


class PostApiView(APIView):
    def get(self,request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailApiView(APIView):
    def get(self, request,pk):
        post = get_object_or_404(Post,pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)
        serializer = PostListSerializer(post)
        return Response(serializer.data)
    def put(self, request,pk):
        post = Post.objects.get(pk=pk)
        serializer = PostSerializer(post, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk):
        post = Post.objects.get(pk=pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





