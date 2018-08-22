from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import redirect

from ubskin_site.column_manage import models as column_models


def get_tree_child_by_columns_id(request):
    '''
    {'id':os.path.join(file_path, i),
    'text':i,
    "children":True,
    'icon':'/static/file_manage/jstree/ico/file.ico'}
    '''
    icon_choices = {
        1: '',
        2: '/static/images/type2.ico',
        3: '',
    }
    data_list = []
    data = None
    data_id = request.GET.get('id')
    if data_id == "#":
        data = column_models.Columns.get_column_link()
        
    else:
        data = column_models.Columns.get_child_data_by_parent_id(data_id)
    if data:
        for i in data:
            data_list.append({
                'id': i['columns_id'],
                'text': i['column_name'],
                "children":True,
                'icon': icon_choices[i['columns_type']]
            })
    return JsonResponse(data_list, safe=False)

def select_tree_item(request):
    return_value = {
        'status': 'error',
        'message': ''
    }
    url_dict = {
        1: reverse('editor_page_content'),
        2: '留言页面',
        3: reverse('shop_manage'),
        4: reverse('article_list'),
        5: reverse('foucs_shop_manage'),
    }
    data_id = request.GET.get('data_id')
    model_obj = column_models.get_model_by_pk(
        column_models.Columns,
        data_id
    )
    if model_obj and model_obj.page_type:
        return_value['data'] = {'url': url_dict[model_obj.page_type]}
        return_value['status'] = 'success'
        return JsonResponse(return_value)
    else:
        return_value['message'] = '元素不存在，请刷新页面'
        return JsonResponse(return_value)
        

def editor_tree_item(request):
    return_value = {
        'status': 'error',
        'message': ''
    }
    url_dict = {
        1: reverse('add_column_link'),
        2: reverse('add_a_page'),
        3: reverse('add_child_column'),
    }
    data_id = request.GET.get('data_id')
    model_obj = column_models.get_model_by_pk(
        column_models.Columns,
        data_id
    )
    return_value['status'] = 'success'
    return_value['data'] = {'url': url_dict[model_obj.columns_type] + '?data_id={}'.format(data_id)}
    return JsonResponse(return_value)

def delete_item_tree(request):
    return_value = {
        'status': 'error',
        'message': '',
    }
    if request.method == 'POST':
        data_id = request.POST.get('data_id')
        column_models.Columns.delete_columns(data_id)
        return_value['status'] = 'success'
        return JsonResponse(return_value)

def delete_articles(request):
    if request.method == 'POST':
        data_id_list = request.POST.getlist('data_id_list[]')
        for i in data_id_list:
            column_models.update_model_data_by_pk(
                column_models.Article,
                i,
                {'status': 'deleted'}
            )
        return JsonResponse({'status': 'success'})


def delete_area(request):
    if request.method == "POST":
        data_id_list = request.POST.getlist('data_id_list[]')
        for i in data_id_list:
            column_models.update_model_data_by_pk(
                column_models.ShopManage,
                i,
                {'status': 'deleted'}
            )
        return JsonResponse({'status': 'success'})

def delete_focus_shop(request):
    if request.method == "POST":
        data_id_list = request.POST.getlist('data_id_list[]')
        for i in data_id_list:
            column_models.update_model_data_by_pk(
                column_models.FocusShop,
                i,
                {'status': 'deleted'}
            )
        return JsonResponse({'status': 'success'})


def request_menu_type(request):
    '''
    var zNodes=[
        {id:-1,pId:0,name:"首页",open:true}
        ,{id:1,pId:-1,name:"管理首页",url:"{% url 'admin_info' %}",target:"iframe_body"}
        ,{id:2,pId:-1,name:"修改密码",url:"{% url 'change_password' %}",target:"iframe_body"}
        ,{id:3,pId:-1,name:"退出登录",url:"{% url 'signout' %}",target:"_parent"}
    ]
    '''
    if request.method == 'GET':
        menu_type = request.GET.get('menu_type')
        if menu_type == 'column_manage':
            return JsonResponse([
                {'id':-1, 'pId':0, 'name':"栏目", 'open':True},
                {'id':1, 'pId':-1, 'name':"栏目管理", 'url': reverse('column_manage'), 'target':"iframe_body"},
            ], safe=False)