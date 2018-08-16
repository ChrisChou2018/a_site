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
    data_id = request.GET.get('data_id')
    column_obj = None
    if data_id is not None:
        column_obj = column_models.get_model_by_pk(
            column_models.Columns,
            data_id,
        )
    if request.method == 'GET':
        if not column_obj:
            return my_render(
                request,
                'column_manage/a_add_column_link.html'
            )
        else:
            return my_render(
                request,
                'column_manage/a_add_column_link.html',
                form_data = column_obj,
            )
    else:
        column_name = request.POST.get('column_name')
        files = request.FILES
        if not column_obj:
            if not column_name:
                return my_render(
                    request,
                    'column_manage/a_add_column_link.html',
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
        return redirect('/myadmin/column_manage/')

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
        if not column_obj:
            return my_render(
                request,
                'column_manage/a_add_a_page.html',
                page_type = page_type,
                columns_select = columns_select,
            )
        else:
            return my_render(
                request,
                'column_manage/a_add_a_page.html',
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
                    'column_manage/a_add_a_page.html',
                    form_data = request.POST,
                    form_errors = from_errors,
                    page_type = page_type,
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
        if not column_obj:
            return my_render(
                request,
                'column_manage/a_add_child_column.html',
                columns_select = column_models.Columns.get_all_select_columns(),
            )
        else:
            return my_render(
                request,
                'column_manage/a_add_child_column.html',
                columns_select = column_models.Columns.get_all_select_columns(data_id),
                form_data = column_obj
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
                    'column_manage/a_add_child_column.html',
                    form_data = request.POST,
                    form_errors = form_errors,
                    columns_select = column_models.Columns.get_all_select_columns(data_id),
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
            article_obj.article_content = article_conten
            article_obj.save()
        return redirect(reverse('editor_page_content'))