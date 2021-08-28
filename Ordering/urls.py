from django.urls import path

from Ordering import views

urlpatterns = [
    path('UpdateCarts/', views.UpdateCarts, name='updateCarts'),
    path('Step_1/', views.Step_1, name='step_1'),
    path('Step_2/', views.Step_2, name='step_2'),
    path('Step_3/', views.Step_3, name='step_3'),
]
