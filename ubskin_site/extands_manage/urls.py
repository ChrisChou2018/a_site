
from django.urls import path

from ubskin_site.extands_manage import views

urlpatterns = [
    path('myadmin/extands_manage/', views.extands_manage, name='extands_manage'),
]

urlpatterns += [
    
]
