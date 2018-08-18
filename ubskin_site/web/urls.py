from django.urls import path

from ubskin_site.web import views

urlpatterns = [
    path('index/', views.index, name='index'),
    # path('location_page/<int: data_id>/', views.location_page, name='location_page'),
    path('public_page/<int:data_id>/', views.public_page, name='public_page'),
    path('', views.index, name='index'),
]
