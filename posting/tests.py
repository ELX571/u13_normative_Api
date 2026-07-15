from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import User
from posting.models import Post
from posting.serializers import PostSerializer

class PostSerializerTest(TestCase):
    def test_valid_post_serializer(self):
        valid_data = {
            "title": "Test Title",
            "content": "This is a valid content that is more than 10 characters."
        }
        serializer = PostSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_post_serializer_short_content(self):
        invalid_data = {
            "title": "Test Title",
            "content": "short"
        }
        serializer = PostSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("Content wrong (content cannot be less than 10)", str(serializer.errors))

    def test_invalid_post_serializer_empty_title(self):
        invalid_data = {
            "title": "",
            "content": "This is a valid content that is more than 10 characters."
        }
        serializer = PostSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertTrue("title" in serializer.errors or "Title wrong" in str(serializer.errors))

class PostPermissionTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="password123")
        self.user2 = User.objects.create_user(username="user2", password="password123")
        self.post1 = Post.objects.create(title="Title 1", content="Content 12345", from_user=self.user1)

        self.list_url = reverse('posts-list')
        self.detail_url = reverse('posts-detail', kwargs={'pk': self.post1.pk})

    def test_create_post_without_auth(self):
        response = self.client.post(self.list_url, {"title": "New Title", "content": "New content text"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_post_not_owner(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.put(self.detail_url, {"title": "Updated", "content": "Updated content here"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_post_owner(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.put(self.detail_url, {"title": "Updated", "content": "Updated content here"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_create_post_with_auth(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(self.list_url, {"title": "New Title", "content": "New content text"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], "New Title")

class PostIntegrationTest(APITestCase):
    def setUp(self):
        self.register_url = '/accounts/auth/register/'
        self.login_url = '/accounts/auth-token/login/'
        self.posts_url = reverse('posts-list')
        
    def test_full_integration_flow(self):
        # 1. Register -> Login -> Token olish
        register_data = {
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "password": "mypassword123",
            "re_password": "mypassword123"
        }
        register_response = self.client.post(self.register_url, register_data)
        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)
        
        login_data = {
            "username": "testuser",
            "password": "mypassword123"
        }
        login_response = self.client.post(self.login_url, login_data)
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        token = login_response.data.get('token')
        self.assertIsNotNone(token)
        
        # Authenticate with token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        
        # 2. Token bilan Post yaratish
        post_data = {
            "title": "Integration Test Post",
            "content": "This is a full integration test content."
        }
        create_post_response = self.client.post(self.posts_url, post_data)
        self.assertEqual(create_post_response.status_code, status.HTTP_201_CREATED)
        post_id = create_post_response.data.get('id')
        self.assertIsNotNone(post_id)
        
        # 3. Post olish
        get_post_url = reverse('posts-detail', kwargs={'pk': post_id})
        get_post_response = self.client.get(get_post_url)
        self.assertEqual(get_post_response.status_code, status.HTTP_200_OK)
        self.assertEqual(get_post_response.data['title'], "Integration Test Post")
        
        # 4. Post update qilish
        update_data = {
            "title": "Updated Integration Test Post",
            "content": "This is an updated full integration test content."
        }
        update_post_response = self.client.put(get_post_url, update_data)
        self.assertEqual(update_post_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_post_response.data['title'], "Updated Integration Test Post")
