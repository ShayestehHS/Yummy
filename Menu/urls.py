from django.urls import path

from Menu import views

urlpatterns = [
    path("AddItem_menu/",views.addItem_form,name="addItem_form"),
    path("DeleteItem_form/", views.deleteItem_form, name="deleteItem_form"),
    path("UpdateItem_form/", views.updateItem_form, name="updateItem_form"),
    path("Filter/<int:page>/", views.filter_restaurants, name="filterAJAX"),
    path("Admin section/",views.admin_section,name="admin_section"),
]
