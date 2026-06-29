from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from posting.models import Post
from posting.serializers import PostSerializer, PostListSerializer
from posting.paginations import CustomPagination
from rest_framework import permissions
from posting.permissions import IsOwnerOrReadOnly


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


class PostModelViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = CustomPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created']

    def get_queryset(self):
        search = self.request.query_params.get('search')
        if search:
            return self.queryset.annotate(
                similarity_title=TrigramSimilarity('title', search),
                similarity_desc=TrigramSimilarity('content', search)
            ).filter(
                Q(similarity_title__gt=0.2) | Q(similarity_desc__gt=0.2)
            ).order_by('-similarity_title')
        return self.queryset

    def perform_create(self, serializer):
        serializer.save(from_user=self.request.user)


class PostViewSet(viewsets.ViewSet):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def list(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(from_user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def update(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
