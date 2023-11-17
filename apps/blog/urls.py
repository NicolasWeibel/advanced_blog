from django.urls import path

from .views import *

urlpatterns = [
    path("list", BlogListView.as_view()),
    path("list/category", ListPostsByCategoryView.as_view()),
    path("detail/<slug>", PostDetailView.as_view()),
    path("search", SearchBlogView.as_view()),
    path("author_list", AuthorBlogListView.as_view()),
    path("author_detail/<slug>", AuthorPostDetailView.as_view()),
    path("edit", EditBlogPostView.as_view()),
]
