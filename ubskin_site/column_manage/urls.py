from django.urls import path

from ubskin_site.column_manage import views, views_js

urlpatterns = [
    path('myadmin/column_manage/', views.column_manage, name='column_manage'),
    path('myadmin/add_column_link/', views.add_column_link, name='add_column_link'),
    path('myadmin/add_a_page/', views.add_a_page, name='add_a_page'),
    path('myadmin/add_child_column/', views.add_child_column, name='add_child_column'),
    path('myadmin/editor_page_content/', views.editor_page_content, name='editor_page_content'),
    path('myadmin/article_list/', views.article_list, name='article_list'),
]

urlpatterns += [
    # path('js/get_tr_str_by_columns_id/', views_js.get_tr_str_by_columns_id, name='get_tr_str_by_columns_id'),
    path('js/get_tree_child_by_columns_id/', views_js.get_tree_child_by_columns_id, name='get_tree_child_by_columns_id'),
    path('js/select_tree_item/', views_js.select_tree_item, name='select_tree_item'),
    path('js/editor_tree_item/', views_js.editor_tree_item, name='editor_tree_item'),
]
