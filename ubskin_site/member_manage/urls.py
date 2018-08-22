from django.urls import path
from ubskin_site.member_manage import views
from ubskin_site.member_manage import views_js

urlpatterns = [
    path('myadmin/signin/', views.member_signin, name='signin'),
    path('myadmin/admin_index/', views.index, name='admin_index'),
    path('myadmin/signout/', views.member_signout, name='signout'),
    path('myadmin/change_password/', views.change_pass, name='change_password'),
    path('myadmin/member_manage/', views.member_manage, name='member_manage'),
    path('myadmin/admin_info/', views.admin_info, name='admin_info'),
    path('myadmin/', views.index),
]


urlpatterns += [
    path('js/create_member/', views_js.create_member, name='create_member'),
    path('js/delete_member/', views_js.delete_member, name='delete_member'),
    path('js/edit_member/', views_js.editor_member, name='edit_member'),
]