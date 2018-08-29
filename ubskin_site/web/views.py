from django.shortcuts import render, redirect
from django.urls import reverse

from ubskin_site.column_manage import models as column_models
from ubskin_site.extends_manage import models as extends_models

# Create your views here.

def my_render(request, templater_path, **kwargs):
    return render(request, templater_path, dict(**kwargs))

def index(request):
    if request.method == "GET":
        column_data = column_models.Columns.build_column_links()
        team_work_data = extends_models.TeamWork.get_team_work_for_index()
        campany_news = column_models.Article.get_campany_news()
        return my_render(
            request,
            'web/index.html',
            column_data = column_data,
            team_work_data = team_work_data,
            campany_news = campany_news,
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
    (5, '重点店铺')
    '''
    model_obj = column_models.get_model_by_pk(
        column_models.Columns,
        data_id
    )
    page = request.GET.get('page', 1)
    column_data_list, select_columns_ids = column_models.Columns.get_page_columns_list(data_id)
    page_type = None
    page_content = None
    data_count = 1
    photo_dict = None
    article_obj = None
    if model_obj.columns_type == 2:
        if model_obj.page_type == 1:
            page_type = 1
            page_content = column_models.Article.get_article_obj_by_columns_id(data_id)
        elif model_obj.page_type == 4:
            article_id = request.GET.get('article_id')
            if article_id:
                article_obj = column_models.get_model_by_pk(
                    column_models.Article,
                    article_id
                )
            page_type = 4
            page_content = column_models.Article.get_article_list_by_columns_id(data_id, page)
            data_count = column_models.Article.get_article_count_by_columns_id(data_id)
        elif model_obj.page_type == 3:
            return redirect(reverse('shop_search', kwargs = {'data_id': model_obj.columns_id}))
        elif model_obj.page_type == 5:
            page_type = 5
            page_content = column_models.FocusShop.get_focus_shops_by_columns_id(data_id, page)
            data_count = column_models.FocusShop.get_focus_shops_count_by_columns_id(data_id)
        elif model_obj.page_type == 2:
            return redirect(reverse('message', kwargs = {'data_id': model_obj.columns_id}))
        photo_dict = {
            'photo_id': model_obj.photo_id,
            'thumb_photo_id': model_obj.thumb_photo_id
        }
    else:
        photo_dict = column_models.Columns.get_prent_photo(model_obj.parent_id)
        page_content = []
    
    column_data = column_models.Columns.build_column_links()
    # print(request.path, '...')
    return my_render(
        request,
        'web/public_page.html',
        column_data_list = column_data_list,
        page_type = page_type,
        page_content = page_content,
        photo_dict = photo_dict,
        column_data = column_data,
        current_page = page,
        data_count = data_count,
        select_columns_ids = select_columns_ids,
        article_obj = article_obj,
        ad_dict = extends_models.Ad.get_ad_dict_for_page,
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

def message(request, data_id):
    column_data = column_models.Columns.build_column_links()
    column_data_list, select_columns_ids = column_models.Columns.get_page_columns_list(data_id)
    model_obj = extends_models.get_model_by_pk(
        column_models.Columns,
        data_id,
    )
    photo_dict = {
        'photo_id': model_obj.photo_id,
        'thumb_photo_id': model_obj.thumb_photo_id
    }
    if request.method == 'GET':
        return my_render(
            request,
            'web/message.html',
            column_data = column_data,
            column_data_list = column_data_list,
            select_columns_ids = select_columns_ids,
            photo_dict = photo_dict,
        )
    else:
        pass