
from django.urls import path

from ubskin_site.extands_manage import views, views_js

urlpatterns = [
    path('myadmin/extands_manage/', views.extands_manage, name='extands_manage'),
    path('myadmin/team_manage/', views.team_manage, name='team_manage'),
    path('myadmin/add_team_work/', views.add_team_work, name='add_team_work'),
]

urlpatterns += [
    path('js/delete_team/', views_js.delete_team, name='delete_team'),
]
