import os

from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse

from ubskin_site.column_manage import models as column_models
from ubskin_site.common import page_image
# Create your views here.


def my_render(request, templater_path, **kwargs):
    return render(request, templater_path, dict(**kwargs))

def column_manage(request):
    if request.method == "GET":
        data_list = column_models.Columns.get_column_table_data()
        return my_render(
            request,
            'column_manage/a_column_manage.html',
            data_list = data_list,
            data_table_head = column_models.Columns.get_style_table_head,
            column_type = dict(column_models.Columns.type_choises),
        )

def add_column_link(request):
    if request.method == 'GET':
        return my_render(
            request,
            'column_manage/a_add_column_link.html'
        )
    else:
        column_name = request.POST.get('column_name')
        if not column_name:
            return my_render(
                request,
                'column_manage/a_add_column_link.html',
                form_data = request.POST,
                form_errors = {'column_name': '不可为空'}
            )
        files = request.FILES
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
        return redirect('/myadmin/column_manage/')

def add_a_page(request):
    page_type = column_models.Columns.page_type_choices
    columns_select = column_models.Columns.get_all_select_columns()
    if request.method == 'GET':
        return my_render(
            request,
            'column_manage/a_add_a_page.html',
            page_type = page_type,
            columns_select = columns_select,
        )
    else:
        column_name = request.POST.get('column_name')
        page_type = request.POST.get('page_type')
        parent_id = request.POST.get('parent_id')
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
                'column_manage/a_add_a_page.html',
                form_data = request.POST,
                form_errors = from_errors,
                page_type = page_type,
                columns_select = columns_select,
            )
        files = request.FILES
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
        return redirect(reverse('column_manage'))

def add_a_child_column(request):
    data_id = request.GET.get('data_id')
    if request.method == 'GET':
        if column_models.Article.has_articlr_by_columns_id(data_id):
            pass
    else:
        pass


def editor_page_content(request):
    data_id = request.GET.get('data_id')
    article_obj = column_models.Article.has_articlr_by_columns_id(data_id)
    if request.method == 'GET':
        if not article_obj :
            return my_render(
                request,
                'column_manage/a_editor_page_conten.html'
            )
        else:
            return my_render(
                request,
                'column_manage/a_editor_page_conten.html',
                form_data = article_obj,
            )
    else:
        article_conten = request.POST.get('article_content')
        if not article_obj:
            column_models.create_model_data(
                column_models.Article,
                {'columns_id': data_id, 'article_content': article_conten}
            )
        else:
            print(article_conten)
            article_obj.article_content = article_conten
            article_obj.save()
        return redirect(reverse('editor_page_content'))
