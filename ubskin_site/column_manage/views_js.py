from django.http import JsonResponse
from django.urls import reverse

from ubskin_site.column_manage import models as column_models



def get_tr_str_by_columns_id(request):
    return_value = {
        'status': 'error',
        'message': ''
    }
    data_id = request.GET.get('data_id')
    data = column_models.Columns.build_child_tr_data(data_id)
    return_value['status'] = 'success'
    return_value['data'] = data
    return JsonResponse(return_value)

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
        3: '/static/images/type3.ico',
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
        3: '物流查询',
        4: '文章列表类型',
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
        
    
    