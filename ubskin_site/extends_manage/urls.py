from django.urls import path

from ubskin_site.extends_manage import views, views_js

urlpatterns = [
    path('myadmin/extends_manage/', views.extends_manage, name='extends_manage'),
    path('myadmin/team_manage/', views.team_manage, name='team_manage'),
    path('myadmin/add_team_work/', views.add_team_work, name='add_team_work'),
    path('myadmin/ad_manage/', views.ad_manage, name='ad_manage'),
    path('myadmin/add_ad/', views.add_ad, name='add_ad'),
    path('myadmin/message_manage/', views.message_manage, name='message_manage'),
]

urlpatterns += [
    path('js/delete_team/', views_js.delete_team, name='delete_team'),
]
