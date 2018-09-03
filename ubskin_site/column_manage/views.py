import os
import time

from django.shortcuts import render
from django.http import HttpResponseRedirect as redirect
from django.http import JsonResponse
from django.conf import settings
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from ubskin_site.column_manage import models as column_models
from ubskin_site.common import page_image
# Create your views here.


def my_render(request, templater_path, **kwargs):
    return render(request, templater_path, dict(**kwargs))

@csrf_exempt
def column_manage(request):
    table_head = column_models.Columns.get_style_table_head()
    column_type_choices = dict(column_models.Columns.type_choises)
    page_type = dict(column_models.Columns.page_type_choices)
    filter_args = None
    data_list = column_models.Columns.get_columns_by_admin()
    if request.method == "GET":
        return my_render(
            request,
            'category/list.html',
            table_head = table_head,
            column_type_choices = column_type_choices,
            page_type = page_type,
            filter_args = filter_args,
            data_list = data_list,
        )
    else:
        classid  = request.GET.get('classid')
        if classid:
            child_data = column_models.Columns.find_child(classid)
            tr_data = ''
            if child_data:
                for i in child_data:
                    tr_str = '<tr id="{}" pId="{}" {} >'.format(
                        i['columns_id'],
                        classid,
                        '' if not i.get('has_child') else 'haschild="true"'
                    )
                    for j in table_head:
                        if j != 'more':
                            if j == 'columns_type':
                                columns_type = column_type_choices[i[j]]
                                tr_str += '<td>{}</td>'.format(columns_type)
                            elif j == 'column_name':
                                tr_str += '<td class="txt_left"><a href="{}" target="_blank">{}</td>'.format(reverse('public_page', kwargs={'data_id': i['columns_id']}), i[j])
                            elif j == 'page_type':
                                tr_str += '<td>{}</td>'.format('' if not i[j] else page_type[i[j]])
                            else:
                                tr_str += '<td>{}</td>'.format(i[j])
                    else:
                        column_type_page_view = {
                            1: 'add_column_link',
                            2: 'add_a_page',
                            3: 'add_child_column',
                        }
                        view_name = column_type_page_view[i['columns_type']]
                        tr_str += '<td><a href="{}">编辑</a>|<a href="{}">删除</a></td>'.format(
                            reverse(view_name) + '?data_id=' + str(i['columns_id']),
                            reverse('delete_item_tree') + '?data_id=' + str(i['columns_id'])
                        )
                        tr_str += '</tr>'
                    tr_data += tr_str
                    
            return JsonResponse(tr_data, safe=False)


def add_column_link(request):
    data_id = request.GET.get('data_id')
    column_obj = None
    if data_id is not None:
        column_obj = column_models.get_model_by_pk(
            column_models.Columns,
            data_id,
        )
    if request.method == 'GET':
        return my_render(
            request,
            'category/add.html',
            form_data = column_obj,
        )

    else:
        column_name = request.POST.get('column_name')
        files = request.FILES
        if not column_obj:
            if not column_name:
                return my_render(
                    request,
                    'category/add.html',
                    form_data = request.POST,
                    form_errors = {'column_name': '不可为空'}
                )
            model_obj = column_models.create_model_data(
                column_models.Columns,
                {'column_name': column_name, "columns_type": 1}
            )
            if files:
                for i in files:
                    file_obj = files[i]
                    if not os.path.exists(settings.MEDIA_ROOT,):
                        os.makedirs(settings.MEDIA_ROOT,)
                    data = page_image.save_upload_photo(
                        file_obj,
                        settings.MEDIA_ROOT,
                    )
                    if data:
                        setattr(model_obj, i, data['photo_id'])
                        model_obj.save()
        else:
            if column_name:
                column_obj.column_name = column_name
                column_obj.save()
            if files:
                for i in files:
                    file_obj = files[i]
                    if not os.path.exists(settings.MEDIA_ROOT,):
                        os.makedirs(settings.MEDIA_ROOT,)
                    data = page_image.save_upload_photo(
                        file_obj,
                        settings.MEDIA_ROOT,
                    )
                    if data:
                        setattr(column_obj, i, data['photo_id'])
                        column_obj.save()
        return redirect(reverse('column_manage'))

def add_a_page(request):
    data_id = request.GET.get('data_id')
    column_obj = None
    if data_id is not None:
        column_obj = column_models.get_model_by_pk(
            column_models.Columns,
            data_id,
        )
    page_type = column_models.Columns.page_type_choices
    columns_select = column_models.Columns.get_all_select_columns()
    if request.method == 'GET':
        return my_render(
            request,
            'category/addpage.html',
            page_type = page_type,
            columns_select = columns_select,
            form_data = column_obj,
        )
        
    else:
        column_name = request.POST.get('column_name')
        page_type = request.POST.get('page_type')
        parent_id = request.POST.get('parent_id')
        files = request.FILES
        if not column_obj:
            from_errors = dict()
            if not column_name:
                from_errors['column_name'] = '不能为空'
            elif not page_type:
                from_errors['page_type'] = '选择一个页面类型'
            elif not parent_id:
                from_errors['parent_id'] = '选择父级元素'
            if from_errors:
                return my_render(
                    request,
                    'category/addpage.html',
                    form_data = request.POST,
                    form_errors = from_errors,
                    page_type = column_models.Columns.page_type_choices,
                    columns_select = columns_select,
                )
            model_obj = column_models.create_model_data(
                column_models.Columns,
                {
                    'column_name': column_name, "columns_type": 2, 'page_type': page_type,
                    'parent_id': parent_id if parent_id else None
                }
            )
            if files:
                for i in files:
                    file_obj = files[i]
                    if not os.path.exists(settings.MEDIA_ROOT,):
                        os.makedirs(settings.MEDIA_ROOT,)
                    data = page_image.save_upload_photo(
                        file_obj,
                        settings.MEDIA_ROOT,
                    )
                    if data:
                        setattr(model_obj, i, data['photo_id'])
                        model_obj.save()
        else:
            if column_name:
                column_obj.column_name = column_name
            if page_type:
                column_obj.page_type = page_type
            if parent_id:
                column_obj.parent_id = parent_id
            column_obj.save()
            if files:
                for i in files:
                    file_obj = files[i]
                    if not os.path.exists(settings.MEDIA_ROOT,):
                        os.makedirs(settings.MEDIA_ROOT,)
                    data = page_image.save_upload_photo(
                        file_obj,
                        settings.MEDIA_ROOT,
                    )
                    if data:
                        setattr(column_obj, i, data['photo_id'])
                        column_obj.save()
        return redirect(reverse('column_manage'))

def add_child_column(request):
    data_id = request.GET.get('data_id')
    column_obj = None
    if data_id is not None:
        column_obj = column_models.get_model_by_pk(
            column_models.Columns,
            data_id,
        )
    if request.method == 'GET':
        return my_render(
            request,
            'category/addlink.html',
            columns_select = column_models.Columns.get_all_select_columns(is_chld_column = True),
            form_data = column_obj,
        )
        
    else:
        column_name = request.POST.get('column_name')
        parent_id = request.POST.get('parent_id')
        if not column_obj:
            form_errors = dict()
            if not column_name:
                form_errors['column_name'] = '不能为空'
            elif not parent_id:
                form_errors['parent_id'] = '选择父级元素'
            if form_errors:
                return my_render(
                    request,
                    'category/addlink.html',
                    form_data = request.POST,
                    form_errors = form_errors,
                    columns_select = column_models.Columns.get_all_select_columns(self_id=data_id, is_chld_column = True),
                )
            column_models.create_model_data(
                column_models.Columns,
                {'column_name': column_name, 'parent_id': parent_id, 'columns_type': 3}
            )
        else:
            column_obj.column_name = column_name
            column_obj.parent_id = parent_id
            column_obj.save()
        return redirect(reverse('column_manage'))

def editor_page_content(request):
    data_id = request.GET.get('data_id')
    article_obj = column_models.Article.has_articlr_by_columns_id(data_id)
    if request.method == 'GET':
        return my_render(
            request,
            'column_manage/a_editor_page_conten.html',
            form_data = article_obj,
            data_id = data_id,
        )
    else:
        article_conten = request.POST.get('article_content')
        if not article_obj:
            column_obj = column_models.get_model_by_pk(
                column_models.Columns,
                data_id
            )
            column_models.create_model_data(
                column_models.Article,
                {'columns_id': data_id, 'article_content': article_conten, 'article_title': column_obj.column_name}
            )
        else:
            article_obj.article_content = article_conten
            article_obj.save()
        return redirect(reverse('editor_page_content'))

def article_list(request):
    search_dict = {
        'search_value': 'article_title__icontains',
        'data_id': 'columns_id',
    }
    search_value = dict()
    current_page = request.GET.get('page', 1)
    filter_args = ""
    for i in search_dict:
        value = request.GET.get(i)
        if value is not None:
            search_value[search_dict[i]] = value
            filter_args  += "&{}={}".format(i, value)
    else:
        if not filter_args:
            filter_args = None
    if search_value:
        data_list = column_models.get_data_list(
            column_models.Article,
            current_page,
            search_value=search_value
        )
        data_count = column_models.get_data_count(
            column_models.Article,
            search_value,
        )
    else:
        data_list = column_models.get_data_list(
            column_models.Article,
            current_page,
        )
        data_count = column_models.get_data_count(
            column_models.Article,
        )
    return my_render(
        request,
        'column_manage/a_article_list.html',
        current_page = current_page,
        form_data = request.GET,
        filter_args = filter_args,
        data_list = data_list,
        data_count = data_count,
        table_head = column_models.Article.get_style_table_head,
    )

def add_article(request):
    columns_id = request.GET.get('columns_id')
    data_id = request.GET.get('data_id')
    model_obj = None
    if data_id:
        model_obj = column_models.get_model_by_pk(
            column_models.Article,
            data_id
        )
    article_type_choices = column_models.Article.article_type_choices
    if request.method == 'GET':
        return my_render(
            request,
            'column_manage/a_add_article.html',
            article_type_choices = article_type_choices,
            form_data = model_obj,
            columns_id = columns_id,
        )
    else:
        article_content = request.POST.get('article_content')
        article_title = request.POST.get('article_title')
        article_type = request.POST.get('article_type', 1)
        description = request.POST.get('description')
        files = request.FILES 
        if not model_obj:
            new_obj = column_models.create_model_data(
                column_models.Article,
                {
                    'article_content': article_content,
                    'article_type': article_type,
                    'article_title': article_title,
                    'create_time': int(time.time()),
                    'columns_id': columns_id,
                    'description': description,
                }
            )
            if files:
                for i in files:
                    file_obj = files[i]
                    if not os.path.exists(settings.MEDIA_ROOT,):
                        os.makedirs(settings.MEDIA_ROOT,)
                    data = page_image.save_upload_photo(
                        file_obj,
                        settings.MEDIA_ROOT,
                    )
                    if data:
                        setattr(new_obj, i, data['photo_id'])
                        new_obj.save()
        else:
            if article_title:
                model_obj.article_title = article_title
            if article_content:
                model_obj.article_content = article_content
            if article_type:
                model_obj.article_type = article_type
            if description:
                model_obj.description = description
            model_obj.save()
            if files:
                for i in files:
                    file_obj = files[i]
                    if not os.path.exists(settings.MEDIA_ROOT,):
                        os.makedirs(settings.MEDIA_ROOT,)
                    data = page_image.save_upload_photo(
                        file_obj,
                        settings.MEDIA_ROOT,
                    )
                    if data:
                        setattr(model_obj, i, data['photo_id'])
                        model_obj.save()
        return JsonResponse({
            'status': 'success',
            'data': reverse('article_list') + '?data_id={}'.format(columns_id)
        })


def shop_manage(request):
    if request.method == "GET":
        search_dict = {
            'search_value': 'shopname__icontains',
        }
        search_value = dict()
        current_page = request.GET.get('page', 1)
        filter_args = ""
        for i in search_dict:
            value = request.GET.get(i)
            if value is not None:
                search_value[search_dict[i]] = value
                filter_args  += "&{}={}".format(i, value)
        else:
            if not filter_args:
                filter_args = None
        if search_value:
            data_list = column_models.get_data_list(
                column_models.ShopManage,
                current_page,
                search_value=search_value
            )
            data_count = column_models.get_data_count(
                column_models.ShopManage,
                search_value,
            )
        else:
            data_list = column_models.get_data_list(
                column_models.ShopManage,
                current_page,
            )
            data_count = column_models.get_data_count(
                column_models.ShopManage,
            )
        return my_render(
            request,
            'column_manage/a_shop_manage.html',
            current_page = current_page,
            form_data = request.GET,
            filter_args = filter_args,
            data_list = data_list,
            data_count = data_count,
            table_head = column_models.ShopManage.get_style_table_head,
        )

def add_area(request):
    data_id = request.GET.get('data_id')
    area_choices = column_models.ShopManage.area_choices
    model_obj = None
    if data_id:
        model_obj = column_models.get_model_by_pk(
            column_models.ShopManage,
            data_id,
        )
    if request.method == "GET":
        return my_render(
            request,
            'column_manage/a_add_area.html',
            area_choices = area_choices,
            form_data = model_obj,
        )
    else:
        p_get = request.POST.get
        shopname = p_get('shopname')
        area = p_get('area')
        address = p_get('address')
        if not model_obj:
            form_errors = dict()
            if not shopname:
                form_errors['shopname'] = '请输入店铺名'
            if not area:
                form_errors['area'] = '请选择地区'
            if form_errors:
                return my_render(
                    request,
                    'column_manage/a_add_area.html',
                    form_data = request.POST,
                    area_choices = area_choices,
                    form_errors = form_errors,
                )
            column_models.create_model_data(
                column_models.ShopManage,
                {'shopname': shopname, 'area': area, 'address': address},
            )
        else:
            if shopname:
                model_obj.shopname = shopname
            if area:
                model_obj.arep = area
            if address:
                model_obj.address
            model_obj.save()
        return redirect(reverse('shop_manage'))

def foucs_shop_manage(request):
    if request.method == "GET":
        search_dict = {
            'data_id': 'columns_id',
            # 'search_value': 'shopname__icontains',
        }
        search_value = dict()
        current_page = request.GET.get('page', 1)
        filter_args = ""
        for i in search_dict:
            value = request.GET.get(i)
            if value is not None:
                search_value[search_dict[i]] = value
                filter_args  += "&{}={}".format(i, value)
        else:
            if not filter_args:
                filter_args = None
        if search_value:
            data_list = column_models.get_data_list(
                column_models.FocusShop,
                current_page,
                search_value
            )
            data_count = column_models.get_data_count(
                column_models.FocusShop,
                search_value,
            )
        else:
            data_list = column_models.get_data_list(
                column_models.FocusShop,
                current_page,
            )
            data_count = column_models.get_data_count(
                column_models.FocusShop,
            )
        return my_render(
            request,
            'column_manage/a_foucs_shop_manage.html',
            current_page = current_page,
            form_data = request.GET,
            filter_args = filter_args,
            data_list = data_list,
            data_count = data_count,
            table_head = column_models.FocusShop.get_style_table_head,
        )

def add_foucs_shop(request):
    columns_id = request.GET.get('columns_id')
    data_id = request.GET.get('data_id')
    shop_selct = column_models.ShopManage.get_all_shop_by_select()
    model_obj = None
    if data_id:
        model_obj = column_models.get_model_by_pk(
            column_models.FocusShop,
            data_id
        )
    if request.method == 'GET':
        return my_render(
            request,
            'column_manage/a_add_foucs_shop.html',
            shop_selct = shop_selct,
            form_data = model_obj,
            columns_id = columns_id,
        )
    else:
        shop_id = request.POST.get('shop_id')
        files = request.FILES
        if not model_obj:
            form_errors = dict()
            if not shop_id:
                form_errors['shop_id'] = '请选择一个店铺'
            if not files:
                form_errors['photo_id'] = '请设置商店图片'
            if form_errors:
                return my_render(
                    request,
                    'column_manage/a_add_foucs_shop.html',
                    shop_selct = shop_selct,
                    form_data = request.POST,
                    form_errors = form_errors,
                    columns_id = columns_id,
                )
            model_obj = column_models.create_model_data(
                column_models.FocusShop,
                {'shop_id': shop_id, 'columns_id': columns_id,}
            )
            if files:
                for i in files:
                    file_obj = files[i]
                    if not os.path.exists(settings.MEDIA_ROOT,):
                        os.makedirs(settings.MEDIA_ROOT,)
                    data = page_image.save_upload_photo(
                        file_obj,
                        settings.MEDIA_ROOT,
                    )
                    if data:
                        setattr(model_obj, i, data['photo_id'])
                        model_obj.save()
        else:
            if shop_id:
                model_obj.shop_id = shop_id
            if files:
                for i in files:
                    file_obj = files[i]
                    if not os.path.exists(settings.MEDIA_ROOT,):
                        os.makedirs(settings.MEDIA_ROOT,)
                    data = page_image.save_upload_photo(
                        file_obj,
                        settings.MEDIA_ROOT,
                    )
                    if data:
                        setattr(model_obj, i, data['photo_id'])
                        model_obj.save()
        
        return redirect(reverse('foucs_shop_manage') + '?data_id=' + columns_id)


def company_addr_manage(request):
    search_dict = {
    }
    search_value = dict()
    current_page = request.GET.get('page', 1)
    filter_args = ""
    for i in search_dict:
        value = request.GET.get(i)
        if value is not None:
            search_value[search_dict[i]] = value
            filter_args  += "&{}={}".format(i, value)
    else:
        if not filter_args:
            filter_args = None
    if search_value:
        data_list = column_models.get_data_list(
            column_models.CompanyAddr,
            current_page,
            search_value=search_value
        )
        data_count = column_models.get_data_count(
            column_models.CompanyAddr,
            search_value,
        )
    else:
        data_list = column_models.get_data_list(
            column_models.CompanyAddr,
            current_page,
        )
        data_count = column_models.get_data_count(
            column_models.CompanyAddr,
        )
    return my_render(
        request,
        'content_manage/company_addr_manage.html',
        current_page = current_page,
        form_data = request.GET,
        filter_args = filter_args,
        data_list = data_list,
        data_count = data_count,
        table_head = column_models.CompanyAddr.get_style_table_head(),
    )

def add_company_addr(request):
    data_id = request.GET.get('data_id')
    model_obj = None
    if data_id:
        model_obj = column_models.get_model_by_pk(
            column_models.CompanyAddr,
            data_id
        )
    if request.method == "GET":
        return my_render(
            request,
            'content_manage/add_company_addr.html',
            form_data = model_obj,
        )
    else:
        fild_list = [
            'company_name', 'phone_number', 'company_addr'
        ]
        p_get = request.POST.get
        if not model_obj:
            form_data = {  i: p_get(i) for i in fild_list if p_get(i) }
            model_obj = column_models.create_model_data(
                column_models.CompanyAddr,
                form_data
            )
            files = request.FILES
            if files:
                for i in files:
                    file_obj = files[i]
                    if not os.path.exists(settings.MEDIA_ROOT,):
                        os.makedirs(settings.MEDIA_ROOT,)
                    data = page_image.save_upload_photo(
                        file_obj,
                        settings.MEDIA_ROOT,
                    )
                    if data:
                        setattr(model_obj, i, data['photo_id'])
                        model_obj.save()
        else:
            for i in fild_list:
                if p_get(i):
                    setattr(model_obj, i, p_get(i))
            else:
                model_obj.save(0)
            files = request.FILES
            if files:
                for i in files:
                    file_obj = files[i]
                    if not os.path.exists(settings.MEDIA_ROOT,):
                        os.makedirs(settings.MEDIA_ROOT,)
                    data = page_image.save_upload_photo(
                        file_obj,
                        settings.MEDIA_ROOT,
                    )
                    if data:
                        setattr(model_obj, i, data['photo_id'])
                        model_obj.save()
        return redirect(reverse('company_addr_manage'))



def page_empty(request):
    return my_render(
        request,
        'content_manage/page_empty.html'
    )