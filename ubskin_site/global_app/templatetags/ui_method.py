import time
import re

from django import template
from django.conf import settings
from django.urls import reverse


from ubskin_site.common import common
from ubskin_site.column_manage import models as column_models


register = template.Library()

@register.simple_tag
def build_photo_url(photo_id, pic_version="thumb", pic_type="photos"):
    # identifier = "!"
    if photo_id:
        return "".join([
            settings.MEDIA_URL, pic_type, "/", pic_version,
            "/", photo_id[:2], "/", photo_id, ".jpg"
        ])
    else:
        return "".join(["/static/", "images/", "user-default.jpg"])



@register.simple_tag
def Pagingfunc(current_page, all_count, filter_args, uri=None):
    try:
        current_page = int(current_page)
    except:
        current_page = 1
    data_num = 15
    a, b = divmod(all_count, data_num)
    if b:
        a = a + 1
    show_page = 10
    all_page = a
    uri = uri if uri is not None else '/'
    filter_args = filter_args if filter_args != None else ''
    html_list = []
    half = int((show_page - 1) / 2)
    start = 0
    stop = 0
    if all_page < show_page:
        start = 1
        stop = all_page
    else:
        if current_page < half + 1:
            start = 1
            stop = show_page
        else:
            if current_page >= all_page - half:
                start = all_page - 10
                stop = all_page
            else:
                start = current_page - half
                stop = current_page + half
    if current_page <= 1:
        previous = """
            <li>
            <a href='#' style='cursor:pointer;text-decoration:none;'>
            上一页<span aria-hidden='true'>&laquo;</span>
            </a>
            </li>
        """
    else:
        previous = """
            <li>
            <a href='{0}?page={1}{2}' class='page_btn'  style='cursor:pointer;text-decoration:none;'>
            上一页<span aria-hidden='true'>&laquo;</span>
            </a>
            </li>
        """.format(uri, current_page - 1, filter_args)
    html_list.append(previous)
    for i in range(start, stop + 1):
        if current_page == i:
            temp = """
                <li>
                <a href='{0}?page={1}{2}' class='page_btn' style='background-color:yellowgreen;cursor:pointer;text-decoration:none;'>
                {3}
                </a>
                </li>
            """.format(uri, i, filter_args, i)
        else:
            temp = """
                <li>
                <a href='{0}?page={1}{2}' class='page_btn' style='cursor:pointer;text-decoration:none;'>
                {3}</a>
                </li>
            """.format(uri, i, filter_args, i)
        html_list.append(temp)
    if current_page >= all_page:
        nex = """
            <li>
            <a href='#' style='cursor:pointer;text-decoration:none;'>
            下一页<span aria-hidden='true'>&raquo;</span>
            </a>
            </li>
        """
    else:
        nex = """
            <li>
            <a href='{0}?page={1}{2}' class='page_btn' style='cursor:pointer;text-decoration:none;'>
            下一页<span aria-hidden='true'>&raquo;</span>
            </a>
            </li>
        """.format(uri, current_page + 1, filter_args)
    html_list.append(nex)
    return ''.join(html_list)


@register.simple_tag
def get_value_by_key(a_dict, key):
    value =  a_dict.get(key)  if a_dict.get(key) is not None else ''
    return value


@register.simple_tag
def get_thumbicon_by_id(photo_id):
    return common.build_photo_url(photo_id)

@register.simple_tag
def parse_timestamps(timestamps):
    t = time.localtime(timestamps)
    time_str = time.strftime(r'%Y-%m-%d %H:%M:%S', t)
    return time_str

@register.simple_tag
def str_step(s, stop):
    if len(s) > stop:
        stop = int(stop)
        return s[:stop] + '...'
    else:
        return s

@register.simple_tag
def str_and_digital(a, b):
    return str(a) == str(b)


@register.simple_tag
def build_child_tr(data_list):
    tr_str = ''
    def build_func(data_list, tr_str, parent_id=None):
        for i in data_list:
            if parent_id is not None:
                tr_str += '''<tr data_id={} parent_id={} style="display: none;"><td>{}{}</td><td>{}</td><td>{}</td><td><a href=''>编辑</a></td></tr>'''.format(
                    i['columns_id'],
                    parent_id ,
                    i['column_name'],
                    '<span class="glyphicon glyphicon-chevron-right"></span>' if i.get('child') else '',
                    i['columns_id'],
                    dict(column_models.Columns.type_choises)[i['columns_type']]    
                )
            else:
                tr_str += '''<tr data_id={}><td>{}{}</td><td>{}</td><td>{}</td><td><a href=''>编辑</a></td></tr>'''.format(
                    i['columns_id'],
                    i['column_name'],
                    '<span class="glyphicon glyphicon-chevron-right"></span>' if i.get('child') else '',
                    i['columns_id'],
                    dict(column_models.Columns.type_choises)[i['columns_type']]
                )
            if i.get('child'):
                return build_func(i['child'], tr_str, parent_id=i['columns_id'])
        else:
            return tr_str
                
    return build_func(data_list, tr_str)


@register.simple_tag
def build_child_select(data_list):
    select_list = list()
    def build_func(data_list, select_list):
        for i in data_list:
            select_list.append(i)
            if i.get('child'):
                return build_func(i['child'], select_list)
        else:
            return select_list
    return build_func(data_list, select_list)


@register.simple_tag
def get_column_name_by_id(data_id):
    return column_models.Columns.get_column_name_by_pk(data_id)


@register.simple_tag
def build_page_tree_column(data_list, select_columns_ids):
    '''
    <li class="subNav currentDd "><a href="javascript:void(null);" title="实体店品牌" >实体店品牌</a></li>
    <li><a href="http://www.ubskin.net/list.asp?classid=2" title="什么是药妆？">什么是药妆？</a></li>
    '''
    li_str = ''
    for i in data_list:
        if i.get('child'):
            li_str += '<li class="subNav {} "><a href="javascript:void(null);" title="{}" >{}</a></li>'.format(
                'currentDd' if i['columns_id'] not in select_columns_ids else 'currentDt',
                i['column_name'],
                i['column_name']
            )
            li_str += '<ul class="left_ul left_ul1" style="{}">'.format(
                '' if i['columns_id'] not in select_columns_ids else 'display:block;'
            )
            for j in i['child']:
                li_str += '<li class="{}"><a href="{}" title="{}">{}</a></li>'.format(
                    '' if j['columns_id'] not in select_columns_ids else 'left_p',
                    reverse('public_page', kwargs={'data_id': j['columns_id']}),
                    j['column_name'],
                    j['column_name']
                )
            else:
                li_str += '</ui>'
        else:
            li_str += '<li class="{}"><a href="{}" title="{}">{}</a></li>'.format(
                '' if i['columns_id'] not in select_columns_ids else 'left_p',
                reverse('public_page', kwargs={'data_id': i['columns_id']}),
                i['column_name'],
                i['column_name']
            )
    return li_str


@register.simple_tag
def get_article_content(content):
    dr = re.compile(r'<[^>]+>',re.S)
    dd = dr.sub('',content)
    return dd[0:50] + '...'
