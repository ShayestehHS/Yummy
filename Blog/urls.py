from django.urls import path

from Blog import views

urlpatterns = [
    path('blogs/<int:page>/', views.Blog_page, name='list_blog'),
    path('<int:blog_id>/', views.Blog_detail, name='detail_blog'),
    path('blogs/<slug:tag_slug>/<int:page>/', views.Blog_tagSearch, name='blog_tagSearch'),
    path('blogs/', views.Blog_search, name='blog_search'),
    path('subscribe/', views.Subscribe, name='subscribe'),
]
