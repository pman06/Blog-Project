from django.urls import path
from . import views
from .feeds import LatestPostsFeed


app_name ='blog'

urlpatterns =[
    path('drafts/', views.DraftListView.as_view(), name='post_draft_list'),
    path('create/', views.CreatePostView.as_view(), name='create'),
    path('edit/<int:pk>', views.PostEditView.as_view(), name='edit'),
    path('delete/<int:pk>', views.PostDeleteView.as_view(), name='delete'),
    path('tags/<slug:tag>', views.Home.as_view(), name='post_by_tag'),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('comment/<int:pk>/approve/', views.comment_approve, name='comment_approve'),
    path('comment/<int:pk>/remove', views.comment_remove, name='comment_remove'),
    path('post/<int:pk>/publish/',views.post_publish, name='post_publish'),
    path('post/<int:id>/share', views.post_share, name = 'post_share'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
    path('search/', views.post_search, name='post_search'),
    path('<slug:slug>/', views.PostDetailView.as_view(), name = 'details'),
]
