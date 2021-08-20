from django.urls import path

from Blog import views

urlpatterns = [
    path('blogs/<int:page>/', views.blog_page, name='list_blog'),
    path('<int:blog_id>/', views.blog_detail, name='detail_blog'),
    path('blogs/<slug:tag_slug>/<int:page>/', views.blog_tag_search, name='blog_tagSearch'),
    path('blogs/', views.blog_search, name='blog_search'),
    path('subscribe/', views.subscribe, name='subscribe'),
]
