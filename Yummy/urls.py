from django.urls import path

from Menu import views as Menu_view
from Yummy import views

urlpatterns = [
    path('', views.Home, name='home'),
    path('list_page/<int:page>/', views.List, name='list'),
    path('grid_list/<int:page>/', views.Grid, name='grid_list'),
    path('menu/<int:id>/', Menu_view.Menu_of_restaurant, name='menu'),
    path('list_page/tag/<slug:tag_slug>/<int:page>/', views.Search_tag, name='list_tag'),
    path('grid_list/tag/<slug:tag_slug>/<int:page>/', views.Search_tag, name='grid_tag'),
    path('sort_restaurants/<int:page>/', views.Sort_restaurants, name='sort_restaurants'),
    path('search/<int:page>/', views.Search, name='search'),
    path('submit_driver/', views.Submit_driver, name='submit_driver'),
    path('submit_restaurant/', views.Submit_restaurant, name='submit_restaurant'),
    path('detail_restaurant/<int:Re_id>/', views.Detail_restaurant, name='detail_restaurant'),
    path('Save_review/<int:Re_id>/', views.Save_review, name='save_review'),
    path('about_us/', views.AboutUs.as_view(), name='about_us'),
    path('Faq/', views.Faq.as_view(), name='faq'),
    path('Contacts/', views.contact_to_us, name='contacts'),
]
