from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework import permissions
from django.db.models.query_utils import Q
from slugify import slugify

from apps.category.models import Category

from .models import Post, ViewCount
from .serializers import (
    AuthorPostListSerializer,
    AuthorPostSerializer,
    PostListSerializer,
    PostSerializer,
)
from .pagination import SmallSetPagination, MediumSetPagination, LargeSetPagination
from .permissions import AuthorPermission, IsPostAuthorOrReadOnly


class BlogListView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        if Post.post_objects.all().exists():
            posts = Post.post_objects.all()

            paginator = SmallSetPagination()
            results = paginator.paginate_queryset(posts, request)

            serializer = PostListSerializer(results, many=True)

            return paginator.get_paginated_response({"posts": serializer.data})
        else:
            return Response(
                {"error": "No posts found"}, status=status.HTTP_404_NOT_FOUND
            )


class ListPostsByCategoryView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        slug = request.query_params.get("slug")

        try:
            category = Category.objects.get(slug=slug)
        except Category.DoesNotExist:
            return Response(
                {"error": "No category found"}, status=status.HTTP_404_NOT_FOUND
            )

        posts = Post.post_objects.order_by("-published").all()

        sub_categories = Category.objects.filter(parent=category)
        filtered_categories = [category]
        for sub_category in sub_categories:
            filtered_categories.append(sub_category)

        posts = posts.filter(category__in=filtered_categories)

        if posts:
            paginator = SmallSetPagination()
            results = paginator.paginate_queryset(posts, request)

            serializer = PostListSerializer(results, many=True)

            return paginator.get_paginated_response({"posts": serializer.data})
        else:
            return Response(
                {"error": "No posts found"}, status=status.HTTP_404_NOT_FOUND
            )


class PostDetailView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, slug, format=None):
        if Post.post_objects.filter(slug=slug).exists():
            post = Post.post_objects.get(slug=slug)
            serializer = PostSerializer(post)

            address = request.META.get("HTTP_X_FORWARDED_FOR")
            if address:
                ip = address.split(",")[-1].strip()
            else:
                ip = request.META.get("REMOTE_ADDR")

            if not ViewCount.objects.filter(post=post, ip_address=ip):
                view = ViewCount(post=post, ip_address=ip)
                view.save()
                post.views = post.get_view_count()
                post.save()

            return Response({"post": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND
            )


class SearchBlogView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        search_term = request.query_params.get("s")
        matches = Post.post_objects.filter(
            Q(title__icontains=search_term)
            | Q(description__icontains=search_term)
            | Q(category__name__icontains=search_term)
        )
        paginator = LargeSetPagination()
        results = paginator.paginate_queryset(matches, request)

        serializer = PostListSerializer(results, many=True)
        return paginator.get_paginated_response({"filtered_posts": serializer.data})


class AuthorBlogListView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        user = self.request.user

        if Post.objects.filter(author=user).exists():
            posts = Post.objects.filter(author=user)

            paginator = SmallSetPagination()
            results = paginator.paginate_queryset(posts, request)

            serializer = AuthorPostListSerializer(results, many=True)

            return paginator.get_paginated_response({"posts": serializer.data})
        else:
            return Response(
                {"error": "No posts found"}, status=status.HTTP_404_NOT_FOUND
            )


class AuthorPostDetailView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, slug, format=None):
        user = self.request.user

        if Post.objects.filter(author=user, slug=slug).exists():
            post = Post.objects.get(author=user, slug=slug)
            serializer = AuthorPostSerializer(post)

            return Response({"post": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND
            )


class EditBlogPostView(APIView):
    permission_classes = (IsPostAuthorOrReadOnly,)
    parser_classes = [MultiPartParser, FormParser]

    def put(self, request, format=None):
        user = self.request.user

        data = self.request.data
        slug = data["slug"]

        print(data)

        post = Post.objects.get(slug=slug)

        if data["title"]:
            if not (data["title"] == "undefined"):
                post.title = data["title"]
                post.save()
        if data["new_slug"]:
            if not (data["new_slug"] == "undefined"):
                post.slug = slugify(data["new_slug"])
                post.save()
        if data["description"]:
            if not (data["description"] == "undefined"):
                post.description = data["description"]
                post.save()
        if data["time_read"]:
            if not (data["time_read"] == "undefined"):
                post.time_read = data["time_read"]
                post.save()
        if data["content"]:
            if not (data["content"] == "undefined"):
                post.content = data["content"]
                post.save()

        if data["category"]:
            if not (data["category"] == "undefined"):
                category_id = int(data["category"])
                category = Category.objects.get(id=category_id)
                post.category = category
                post.save()

        if data["thumbnail"]:
            if not (data["thumbnail"] == "undefined"):
                post.thumbnail = data["thumbnail"]
                post.save()

        return Response({"success": "Post edited"})


class DraftBlogPostView(APIView):
    permission_classes = (IsPostAuthorOrReadOnly,)

    def put(self, request, format=None):
        data = self.request.data
        slug = data["slug"]

        post = Post.objects.get(slug=slug)

        post.status = "draft"
        post.save()

        return Response({"success": "Post edited"})


class PublishBlogPostView(APIView):
    permission_classes = (IsPostAuthorOrReadOnly,)

    def put(self, request, format=None):
        data = self.request.data
        slug = data["slug"]

        post = Post.objects.get(slug=slug)

        post.status = "published"
        post.save()

        return Response({"success": "Post edited"})


class DeleteBlogPostView(APIView):
    permission_classes = (IsPostAuthorOrReadOnly,)

    def delete(self, request, slug, format=None):
        post = Post.objects.get(slug=slug)

        post.delete()

        return Response({"success": "Post edited"})


class CreateBlogPostView(APIView):
    permission_classes = (AuthorPermission,)

    def post(self, request, format=None):
        user = self.request.user
        Post.objects.create(author=user)

        return Response({"success": "Post edited"})
