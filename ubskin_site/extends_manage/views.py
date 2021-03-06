from django.shortcuts import render

# Create your views here.
import os

from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse

from ubskin_site.extends_manage import models as extends_models
from ubskin_site.column_manage import models as column_models
from ubskin_site.common import page_image
# Create your views here.

def my_render(request, templater_path, **kwargs):
    return render(request, templater_path, dict(**kwargs))

def extends_manage(request):
    if request.method == "GET":
        return my_render(
            request,
            'extends_manage/extends_manage.html'
        )

def team_manage(request):
    if request.method == "GET":
        search_dict = {
            'team_name': 'team_name__icontains',
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
            data_list = extends_models.get_data_list(
                extends_models.TeamWork,
                current_page,
                search_value=search_value
            )
            data_count = extends_models.get_data_count(
                extends_models.TeamWork,
                search_value,
            )
        else:
            data_list = extends_models.get_data_list(
                extends_models.TeamWork,
                current_page,
            )
            data_count = extends_models.get_data_count(
                extends_models.TeamWork,
            )
        return my_render(
            request,
            'extends_manage/team_manage.html',
            current_page = current_page,
            form_data = request.GET,
            filter_args = filter_args,
            data_list = data_list,
            data_count = data_count,
            table_head = extends_models.TeamWork.get_style_table_head,
            team_dict = dict(extends_models.TeamWork.team_choices),
        )

def add_team_work(request):
    data_id = request.GET.get('data_id')
    model_obj = None
    if data_id:
        model_obj = extends_models.get_model_by_pk(
            extends_models.TeamWork,
            data_id,
        )
    team_choices = extends_models.TeamWork.team_choices
    if request.method == "GET":
        return my_render(
            request,
            'extends_manage/add_team_work.html',
            team_choices = team_choices,
            form_data = model_obj,
        )
    else:
        p_get = request.POST.get
        team_name = p_get('team_name')
        team_link = p_get('team_link', '#a')
        team_type = p_get('team_type')
        files = request.FILES
        if not model_obj:
            form_errors = dict()
            if not team_name:
                form_errors['team_name'] = '请输入合作商名称'
            if not team_type:
                form_errors['team_type'] = '请输入合作商类型'
            if form_errors:
                return my_render(
                    request,
                    'extends_manage/add_team_work.html',
                    team_choices = team_choices,
                    form_data = request.POST,
                    form_errors = form_errors
                )
            model_obj = extends_models.create_model_data(
                extends_models.TeamWork,
                {'team_name': team_name, 'team_type': team_type, 'team_link': team_link,}
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
            if team_name:
                model_obj.team_name = team_name
            if team_link:
                model_obj.team_link = team_link
            if team_type:
                model_obj.team_type = team_type
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
        return redirect(reverse('team_manage'))


def ad_manage(request):
    if request.method == "GET":
        search_dict = {
            'team_name': 'team_name__icontains',
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
            data_list = extends_models.get_data_list(
                extends_models.Ad,
                current_page,
                search_value=search_value
            )
            data_count = extends_models.get_data_count(
                extends_models.Ad,
                search_value,
            )
        else:
            data_list = extends_models.get_data_list(
                extends_models.Ad,
                current_page,
            )
            data_count = extends_models.get_data_count(
                extends_models.Ad,
            )
        return my_render(
            request,
            'extends_manage/ad_manage.html',
            current_page = current_page,
            form_data = request.GET,
            filter_args = filter_args,
            data_list = data_list,
            data_count = data_count,
            table_head = extends_models.Ad.get_style_table_head,
            location_choices = dict(extends_models.Ad.location_choices)
        )

def add_ad(request):
    data_id = request.GET.get('data_id')
    model_obj = None
    if data_id:
        model_obj = extends_models.get_model_by_pk(
            extends_models.Ad,
            data_id
        )
    if request.method == 'GET':
        return my_render(
            request,
            'extends_manage/add_ad.html',
            form_data = model_obj,
            location_choices = extends_models.Ad.location_choices,
            page_select = column_models.Columns.get_all_page_for_select(),
        )
    else:
        filds_list = [
            'ad_name', 'ad_title', 'ad_e_title',
            'ad_text', 'columns_id', 'location',
        ]
        cant_empty = {
            'ad_name': '广告名不可为空',
            'ad_title': '广告标题不可为空',
        }
        p_get = request.POST.get
        if not model_obj:
            form_errors = dict()
            for i in cant_empty:
                d = p_get(i)
                if not d:
                    form_errors[i] = cant_empty[i]
            if form_errors:
                return my_render(
                    request,
                    'extends_manage/add_ad.html',
                    form_data = model_obj,
                    location_choices = extends_models.Ad.location_choices,
                    page_select = column_models.Columns.get_all_page_for_select(),
                    form_errors = form_errors
                )
            form_data = { i:p_get(i) for i in filds_list if p_get(i) }
            model_obj = extends_models.create_model_data(
                extends_models.Ad,
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
            for i in filds_list:
                if p_get(i):
                    setattr(model_obj, i, p_get(i))
            else:
                model_obj.save()
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
        return redirect(reverse('ad_manage'))

def message_manage(request):
    if request.method == "GET":
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
            data_list = extends_models.get_data_list(
                extends_models.Message,
                current_page,
                search_value=search_value
            )
            data_count = extends_models.get_data_count(
                extends_models.Message,
                search_value,
            )
        else:
            data_list = extends_models.get_data_list(
                extends_models.Message,
                current_page,
            )
            data_count = extends_models.get_data_count(
                extends_models.Message,
            )
        return my_render(
            request,
            'extends_manage/message_manage.html',
            current_page = current_page,
            form_data = request.GET,
            filter_args = filter_args,
            data_list = data_list,
            data_count = data_count,
            table_head = extends_models.Message.get_style_table_head(),
        )

def check_message(request):
    if request.method == "GET":
        data_id = request.GET.get('data_id')
        model_obj = extends_models.get_model_by_pk(
            extends_models.Message,
            data_id
        )
        return my_render(
            request,
            'extends_manage/check_message.html',
            form_data = model_obj
        )