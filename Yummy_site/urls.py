"""Yummy_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.base, name='base')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='base')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from Yummy import views as views_yummy

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Yummy => urls
    path('', include('Yummy.urls')),
    # path('', views.Home, name='home'),
    # path('list_page/<int:page>/', views.List, name='list'),
    # path('grid_list/<int:page>/', views.Grid, name='grid_list'),
    # path('menu/<int:id>/', Menu_view.Menu_of_restaurant, name='menu'),
    # path('list_page/tag/<slug:tag_slug>/<int:page>/', views.Search_tag, name='list_tag'),
    # path('grid_list/tag/<slug:tagSlug>/<int:page>/', views.Search_tag, name='grid_tag'),
    # path('sort_restaurants/<int:page>/', views.Sort_restaurants, name='sort_restaurants'),
    # path('search/<int:page>/', views.Search, name='search'),
    # path('submit_driver/', views.Submit_driver, name='submit_driver'),
    # path('submit_restaurant/', views.Submit_restaurant, name='submit_restaurant'),
    # path('detail_restaurant/<int:Re_id>/', views.Detail_restaurant, name='detail_restaurant'),
    # path('Save_review/<int:Re_id>/', views.Save_review, name='save_review'),
    # path('about_us/', views.About_us.as_view(), name='about_us'),
    # path('Faq/', views.Faq.as_view(), name='faq'),
    # path('Contacts/', views.Contacts, name='contacts'),

    # Users => urls
    path('Users/', include('Users.urls')),
    # path('Register/', views.Register_Login, name='register'),
    # path('Login/', views.Login, name='login'),
    # path('Logout/', views.Logout, name='logout'),
    # path('SignUp/', views.SignUp, name='sign_up'),
    # path('ConfirmEmail/<str:UserCode>/', views.Confirm_email, name='ConfirmEmail'),
    # path('Accounts/', include('allauth.urls')),
    # # django views
    # path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Blog => urls
    path('Blog/', include('Blog.urls')),
    # path('blogs/<int:page>/', views.Blog_page, name='list_blog'),
    # path('<int:blog_id>/', views.Blog_detail, name='detail_blog'),
    # path('blogs/<slug:tag_slug>/<int:page>/', views.Blog_tagSearch, name='blog_tagSearch'),
    # path('blogs/', views.Blog_search, name='blog_search'),
    # path('subscribe/', views.Subscribe, name='subscribe'),

    # Ordering => urls
    path('Ordering/',include('Ordering.urls')),
    # path('UpdateCarts/', views.UpdateCarts, name='UpdateCarts'),
    # path('Step_1/', views.Step_1, name='step_1'),
    # path('Step_2/', views.Step_2, name='step_2'),
    # path('Step_3/', views.Step_3, name='step_3'),

    # Menu => urls
    path('Menu/',include('Menu.urls')),
    # path("AddItem_menu/", views.addItem_form, name="addItem_form"),
    # path("DeleteItem_form/", views.deleteItem_form, name="deleteItem_form"),
    # path("UpdateItem_form/", views.updateItem_form, name="updateItem_form"),
    # path("Filter/<int:page>/", views.filter_restaurants, name="filterAJAX"),
    # path("Admin section/", views.admin_section, name="admin_section"),

    # django-comment-xtd
    path(r'comments/', include('django_comments_xtd.urls')),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
