from django.urls import path

from ubskin_site.web import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('public_page/<int:data_id>/', views.public_page, name='public_page'),
    path('shop_search/<int:data_id>/', views.shop_search, name='shop_search'),
    path('', views.index, name='index'),
]
