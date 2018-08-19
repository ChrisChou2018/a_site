from django.shortcuts import render, redirect
from django.urls import reverse

from ubskin_site.column_manage import models as column_models

# Create your views here.

def my_render(request, templater_path, **kwargs):
    return render(request, templater_path, dict(**kwargs))

def index(request):
    if request.method == "GET":
        column_data = column_models.Columns.build_column_links()
        return my_render(
            request,
            'web/index.html',
            column_data = column_data
        )


def public_page(request, data_id):
    '''
    (1, '导航栏目'),
    (2, '单网页'),
    (3, '菜单'),
    -----
    (1, '文本图片'),
    (2, '留言页面'),
    (3, '物流查询'),
    (4, '文章列表类型'),
    '''
    model_obj = column_models.get_model_by_pk(
        column_models.Columns,
        data_id
    )
    select_columns_ids = list()
    column_data_list = column_models.Columns.get_page_columns_list(data_id)
    page_type = None
    page_content = None
    photo_dict = None
    if model_obj.columns_type == 2:
        if model_obj.page_type == 1:
            select_columns_ids.append(model_obj.columns_id)
            parent_obj = column_models.get_model_by_pk(
                column_models.Columns,
                model_obj.parent_id
            )
            if parent_obj.columns_type != 1:
                select_columns_ids.append(parent_obj.columns_id)
            page_type = 1
            page_content = column_models.Article.get_article_obj_by_columns_id(data_id)
        elif model_obj.page_type == 4:
            select_columns_ids.append(model_obj.columns_id)
            page_type = 4
            page_content = column_models.Article.get_article_list_by_columns_id(data_id)
        elif model_obj.page_type == 3:
            return redirect(reverse('shop_search', kwargs = {'data_id': model_obj.columns_id}))
        photo_dict = {
            'photo_id': model_obj.photo_id,
            'thumb_photo_id': model_obj.thumb_photo_id
        }
    else:
        photo_dict = column_models.Columns.get_prent_photo(model_obj.parent_id)
        page_content = []
    
    column_data = column_models.Columns.build_column_links()
    return my_render(
        request,
        'web/public_page.html',
        column_data_list = column_data_list,
        page_type = page_type,
        page_content = page_content,
        photo_dict = photo_dict,
        column_data = column_data,
        select_columns_ids = select_columns_ids,
    )
    

def shop_search(request, data_id):
    column_data = column_models.Columns.build_column_links()
    model_obj = column_models.get_model_by_pk(
        column_models.Columns,
        data_id
    )
    shop_data_dict = column_models.ShopManage.get_all_shop_for_search()
    photo_dict = {
        'photo_id': model_obj.photo_id,
        'thumb_photo_id': model_obj.thumb_photo_id
    }
    return my_render(
        request,
        'web/shop_search.html',
        column_data = column_data,
        photo_dict = photo_dict,
        shop_data_dict = shop_data_dict,
    )