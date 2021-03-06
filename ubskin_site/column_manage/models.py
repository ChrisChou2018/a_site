import time

from django.db import models
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models import Count
from django.urls import reverse


class Columns(models.Model):
    '''
    菜单栏表
    '''
    columns_id = models.AutoField(db_column="columns_id", primary_key=True, verbose_name="菜单栏ID")
    column_name = models.CharField(db_column="column_name", verbose_name="菜单栏名称", max_length=255)
    type_choises = (
        (1, '导航栏目'),
        (2, '单网页'),
        (3, '子栏目'),
    )
    columns_type = models.SmallIntegerField(choices=type_choises, db_column='columns_type', verbose_name='菜单类型')
    link = models.CharField(db_column="link", verbose_name="链接地址", max_length=1000, null=True, blank=True)
    photo_id = models.CharField(db_column="photo_id", null=True, blank=True, verbose_name='图片ID', max_length=255)
    thumb_photo_id = models.CharField(db_column="thumb_photo_id", null=True, blank=True, verbose_name='小图片ID', max_length=255)
    parent_id = models.BigIntegerField(db_column='parent_id', verbose_name='父级菜单ID', null=True, blank=True,)
    page_type_choices = (
        (1, '文本图片页面'),
        (2, '留言页面'),
        (3, '店铺查询页面'),
        (4, '文章列表页面'),
        (5, '公司地址页面'),
        (6, '重点店铺页面'),
    )
    page_type = models.SmallIntegerField(choices=page_type_choices, db_column='page_type', verbose_name='单页面类型', null=True, blank=True)
    has_scrolling_image = models.BooleanField(db_column="has_scrolling_image", verbose_name="是否有轮播图", default=False)
    order_num = models.SmallIntegerField(db_column='order_num', verbose_name='排序数', default=1)
    status = models.CharField(db_column="status", verbose_name="数据状态", default="normal", max_length=255)
    


    class Meta:
        db_table = 'columns'
    
    @classmethod
    def get_all_select_columns(cls, self_id=None, is_chld_column=False):
        column_index_list = cls.objects.filter(columns_type=1, status='normal').values('columns_id', 'column_name')
        child = None
        if not column_index_list:
            return list()
        for i in column_index_list:
            if self_id:
                child = cls.objects.filter(~Q(columns_id=self_id), parent_id=i['columns_id'], status='normal', columns_type=3).values('columns_id', 'column_name')
            else:
                child = cls.objects.filter(parent_id=i['columns_id'], status='normal', columns_type=3).values('columns_id', 'column_name')
            if child and not is_chld_column:
                for j in child:
                    j['column_name'] = i['column_name'] + '__' + j['column_name']
                i['child'] = child
        return column_index_list
    
    @classmethod
    def get_column_link(cls):
        return cls.objects.filter(columns_type=1, status='normal').values()
    
    @classmethod
    def get_child_data_by_parent_id(cls, data_id):
        return cls.objects.filter(status='normal', parent_id=data_id).values()

    @classmethod
    def get_column_name_by_pk(cls, data_id):
        obj = cls.objects.filter(pk=data_id).first()
        return obj.column_name if obj else '空'
    
    @classmethod
    def delete_columns(cls, data_id):
        id_list = list()
        id_list.append(data_id)
        def find_all_child(data_id, id_list):
            child = cls.objects.filter(status='normal', parent_id=data_id).values()
            if child:
                for i in child:
                    id_list.append(i['columns_id'])
                    find_all_child(i['columns_id'], id_list)
            return id_list
        id_list = find_all_child(data_id, id_list)
        cls.objects.filter(pk__in=id_list, status='normal').update(status='deleted')
        Article.objects.filter(status='normal', columns_id__in=id_list).update(status='deleted')
    
    @classmethod
    def build_column_links(cls):
        data_list = cls.objects.filter(columns_type=1, status='normal').values()
        for i in data_list:
            child = cls.objects.filter(parent_id=i['columns_id'], status='normal').values()
            if child:
                i['child'] = child
        return data_list
    
    @classmethod
    def get_page_columns_list(cls, data_id):
        select_columns_ids = set()
        select_columns_ids.add(data_id)
        def find_all_child(data_list):
            for i in data_list:
                child = cls.objects.filter(status='normal', parent_id=i['columns_id']).values()
                if child:
                    i['child'] = find_all_child(child)
            else:
                return data_list
        obj = cls.objects.filter(columns_id = data_id, status = 'normal').first()
        if obj:
            parent_obj = cls.objects.filter(status='normal', columns_id=obj.parent_id).first()
            select_columns_ids.add(parent_obj.columns_id)
            if parent_obj.columns_type == 3:
                parent_obj = cls.objects.filter(status='normal', columns_id=parent_obj.parent_id).first()
                select_columns_ids.add(parent_obj.columns_id)
            child_list = cls.objects.filter(status='normal', parent_id=parent_obj.columns_id).values()
            data_list = find_all_child(child_list)
            return data_list, select_columns_ids
        else:
            return list(), select_columns_ids
    
    @classmethod
    def get_prent_photo(cls, data_id):
        photo_dict = dict()
        parent_obj = cls.objects.filter(columns_id=data_id, status='normal').first()
        photo_dict['photo_id'] = parent_obj.photo_id
        photo_dict['thumb_photo_id'] = parent_obj.thumb_photo_id
        return photo_dict
    
    @classmethod
    def get_style_table_head(cls):
        return dict(
            column_name = '栏目名称',
            columns_id = '菜单栏ID',
            columns_type = '栏目类型',
            page_type = '页面类型',
            more = '更多'
        )

    @classmethod
    def get_columns_by_admin(cls):
        data_list = cls.objects.filter(columns_type=1, status='normal').values()
        for i in data_list:
            child  = cls.objects.filter(parent_id=i['columns_id'], status='normal')
            if child:
                i['has_child'] = True
        return data_list
    
    @classmethod
    def find_child(cls, data_id):
        data_list = cls.objects.filter(parent_id=data_id, status='normal').values()
        for i in data_list:
            child = cls.objects.filter(parent_id=i['columns_id'],  status='normal').values()
            if child:
                i['has_child'] = True
        return data_list
    
    @classmethod
    def build_column_tree(cls):
        '''
        {'id':-1, 'pId':0, 'name':"栏目", 'open':True},
        {'id':1, 'pId':-1, 'name':"栏目管理", 'url': reverse('column_manage'), 'target':"iframe_body"},
        '''
        data = cls.objects.filter(status='normal').values().order_by('pk')
        data_list = list()

        x = 1
        for i in data:
            if i['columns_type'] == 1:
                if x == 1:
                    data_list.append({
                        'id': i['columns_id'], 'pId': i['parent_id'] if i['parent_id'] else 0,
                        'name': i['column_name'], 'open': True
                    })
                else: 
                    data_list.append({
                        'id': i['columns_id'], 'pId': i['parent_id'] if i['parent_id'] else 0,
                        'name': i['column_name'],
                    })
                x += 1
            elif i['columns_type'] == 2:
                url_dict = {
                    1: reverse('editor_page_content'),
                    2: reverse('message_manage'),
                    3: reverse('shop_manage'),
                    4: reverse('article_list'),
                    5: reverse('company_addr_manage'),
                    6: reverse('foucs_shop_manage'),
                }
                data_list.append({
                        'id': i['columns_id'], 'pId': i['parent_id'] if i['parent_id'] else 0,
                        'name': i['column_name'], 'url': url_dict[i['page_type']] + '?data_id=' + str(i['columns_id']),
                        'target':"iframe_body",
                    })
            else:
                data_list.append({
                        'id': i['columns_id'], 'pId': i['parent_id'] if i['parent_id'] else 0,
                        'name': i['column_name'],
                    })
        if data_list:
            return data_list
        else:
            return [{'id':-1, 'pId':0, 'name':"内容", 'open':True},{'id':1, 'pId':-1, 'name':"空", 'url': reverse('page_empty'), 'target':"iframe_body"}]
    
    @classmethod
    def get_all_page_for_select(cls):
        data_list = cls.objects.filter(columns_type=2, status='normal').values_list('columns_id', 'column_name')
        return data_list


class Article(models.Model):

    article_id  = models.AutoField(db_column="article_id", primary_key=True, verbose_name="文章ID")
    columns_id = models.BigIntegerField(db_column="columns_id", verbose_name="所属栏目ID", null=True, blank=True)
    article_type_choices = (
        (1, '普通文章类型'),
        (2, '大图片标题类型'),
    )
    article_type = models.SmallIntegerField(db_column='article_type', verbose_name='文章列表类型', default=1)
    article_title = models.CharField(db_column="article_title", verbose_name="文章标题", max_length=255, null=True, blank=True)
    description = models.CharField(db_column="description", verbose_name="简短说明", max_length=1000, null=True, blank=True)
    article_content = models.TextField(db_column="article_content", verbose_name="文章内容", null=True, blank=True)
    photo_id = models.CharField(db_column="photo_id", null=True, blank=True, verbose_name='图片ID', max_length=255)
    create_time = models.IntegerField(db_column="create_time", verbose_name="创建时间", default=int(time.time()))
    read_colunt = models.IntegerField(db_column='read_colunt', verbose_name='阅读量', default=0)
    status = models.CharField(db_column="status", verbose_name="数据状态", default="normal", max_length=255)


    class Meta:
        db_table = 'article'
    

    @classmethod
    def get_style_table_head(cls):
        return dict(
            article_id = '文章ID',
            article_title = '文章标题',
            read_colunt = '人气',
            columns_id = '所属栏目',
            more = '更多'
        )

    @classmethod
    def get_article_obj_by_columns_id(cls, columns_id):
        return cls.objects.filter(columns_id=columns_id, status='normal').first()
    
    @classmethod
    def get_article_list_by_columns_id(cls, columns_id, current_page):
        data_list = cls.objects.filter(columns_id=columns_id, status='normal')
        p = Paginator(data_list, 15)
        return p.page(current_page).object_list.values()
    
    @classmethod
    def get_article_count_by_columns_id(cls, data_id):
        return cls.objects.filter(status='normal', columns_id=data_id).count()

    @classmethod
    def has_articlr_by_columns_id(cls, data_id):
        return cls.objects.filter(columns_id=data_id, status='normal').first()
    
    @classmethod
    def get_campany_news(cls):
        company_active = Columns.objects.filter(column_name='企业动态', status='normal').first()
        data_list = None
        if company_active:
            data_list = cls.objects.filter(columns_id=company_active.columns_id, status='normal').order_by('-pk')[0:8]
        return data_list if data_list else list()


class ColumnScrollingImage(models.Model):
    scrolling_image_id = models.AutoField(db_column="scrolling_image_id", primary_key=True, verbose_name="滚动图ID")
    columns_id = models.BigIntegerField(db_column="columns_id")
    photo_id = models.CharField(db_column="photo_id", null=True, blank=True, verbose_name='图片ID', max_length=255)
    file_size = models.CharField(db_column="file_size", verbose_name="文件大小", max_length=255)
    resolution = models.CharField(db_column="resolution", verbose_name="分辨率", max_length=255)
    file_type  = models.CharField(db_column="file_type", verbose_name="文件类型", max_length=255)
    status = models.CharField(db_column="status", verbose_name="数据状态", default="normal", max_length=255)


    class Meta:
        db_table = 'column_scrolling_image'


class ShopManage(models.Model):
    shop_id = models.AutoField(db_column="shop_id", primary_key=True, verbose_name="店铺ID")
    shopname = models.CharField(db_column="shopname", verbose_name='店铺名称', max_length=255)
    area_choices = [
        ['shaanxi', '陕西'],
        ['hebei', '河北'],
        ['shanxi', '山西'],
        ['liaoning', '辽宁'],
        ['jilin', '吉林'],
        ['heilongjiang', '黑龙江'],
        ['jiangsu', '江苏'],
        ['zhejiang', '浙江'],
        ['anhui', '安徽'],
        ['fujian', '福建'],
        ['jiangxi', '江西'],
        ['shandong', '山东'],
        ['henan', '河南'],
        ['hubei', '湖北'],
        ['hunan', '湖南'],
        ['guangdong', '广东'],
        ['hainan', '海南'],
        ['sichuan', '四川'],
        ['guizhou', '贵州'],
        ['yunnan', '云南'],
        ['gansu', '甘肃'],
        ['qinghai', '青海'],
        ['aiwan', '台湾'],
        ['eimongol', '内蒙古'],
        ['guangxi', '广西'],
        ['xizang', '西藏'],
        ['gxia', '宁夏'],
        ['xinjiang', '新疆'],
        ['beijing', '北京'],
        ['anjin', '天津'],
        ['shanghai', '上海'],
        ['chongqing', '重庆']
    ]
    area = models.CharField(db_column="area", verbose_name='所在地区', max_length=255, choices=area_choices)
    address = models.CharField(db_column="address", verbose_name='所在地区', max_length=2000, null=True, blank=True)
    status = models.CharField(db_column="status", verbose_name="数据状态", default="normal", max_length=255)


    class Meta:
        db_table = 'shop_manage'
    

    @classmethod
    def get_all_shop_for_search(cls):
        data_dict = dict()
        data_list = cls.objects.filter(status='normal').values('area').annotate(c=Count('area'))
        if data_list:
            for i in data_list:
                obj_list = cls.objects.filter(area=i['area']).values()
                if obj_list:
                    data_dict[i['area']] = obj_list
            else:
                return data_dict
        else:
            return {}
    
    @classmethod
    def get_shopname_by_shop_id(cls, shop_id):
        model_obj = cls.objects.filter(pk=shop_id).first()
        return model_obj.shopname if model_obj else '店铺已尽删除'
    
    @classmethod
    def get_all_shop_by_select(cls):
        data_list = cls.objects.filter(status='normal').values_list('shop_id', 'shopname')
        return data_list if data_list else None
    
    @classmethod
    def get_style_table_head(cls):
        return dict(
            shop_id = '店铺ID',
            shopname = '店铺名称',
            area = '所在地区',
            more = '更多'
        )


class FocusShop(models.Model):
    focus_shop_id = models.AutoField(db_column="focus_shop_id", primary_key=True, verbose_name="重点店铺ID")
    columns_id = models.IntegerField(db_column="columns_id", verbose_name="所属栏目ID", null=True, blank=True)
    shop_id = models.IntegerField(db_column="shop_id", verbose_name="店铺ID", null=True, blank=True)
    photo_id = models.CharField(db_column="photo_id", null=True, blank=True, verbose_name='店铺图ID', max_length=255)
    status = models.CharField(db_column="status", verbose_name="数据状态", default="normal", max_length=255)


    class Meta:
        db_table = 'focus_shop'


    @classmethod
    def get_style_table_head(cls):
        return dict(
            focus_shop_id = '重点店铺ID',
            shop_id = '店铺名称',
            more = '更多',
        )

    @classmethod
    def get_focus_shops_by_columns_id(cls, columns_id, current_page):
        data_list = cls.objects.filter(status='normal', columns_id=columns_id)
        p = Paginator(data_list, 15)
        return p.page(current_page).object_list.values()
    
    @classmethod
    def get_focus_shops_count_by_columns_id(cls, columns_id):
        return cls.objects.filter(status='normal', columns_id=columns_id).count()


class CompanyAddr(models.Model):
    company_addr_id = models.AutoField(db_column="company_addr_id", primary_key=True, verbose_name="公司地址ID")
    company_name = models.CharField(db_column="company_name", null=True, blank=True, verbose_name='公司名称', max_length=255)
    phone_number = models.CharField(db_column="phone_number", null=True, blank=True, verbose_name='公司电话', max_length=255)
    company_addr = models.CharField(db_column="company_addr", null=True, blank=True, verbose_name='公司地址', max_length=255)
    photo_id = models.CharField(db_column="photo_id", null=True, blank=True, verbose_name='公司图', max_length=255)
    status = models.CharField(db_column="status", verbose_name="数据状态", default="normal", max_length=255)

    class Meta:
        db_table = 'company_addr'


    @classmethod
    def get_style_table_head(cls):
        return dict(
            company_addr_id = '公司地址ID',
            company_name = '公司名称',
            phone_number = '公司电话',
            company_addr = '公司地址',
            more = '更多',
        )


def get_data_list(model, current_page, search_value=None, order_by="-pk", search_value_type='dict'):
    if search_value:
        if search_value_type == 'dict':
            data_list = model.objects.filter(**search_value, status='normal'). \
                order_by(order_by)
        else:
            data_list = model.objects.filter(search_value, status='normal'). \
                order_by(order_by)
    else:
        data_list = model.objects.filter(status='normal'). \
            order_by(order_by)
    p = Paginator(data_list, 15)
    return p.page(current_page).object_list.values()


def get_data_count(model, search_value=None, search_value_type='dict'):
    if search_value:
        if search_value_type == 'dict':
            count = model.objects.filter(**search_value, status='normal').count()
        else:
            count = model.objects.filter(search_value, status='normal').count()
    else:
        count = model.objects.filter(status='normal').count()
    return count

def create_model_data(model, data):
    return model.objects.create(**data)


def get_model_by_pk(model, pk):
    try:
        return model.objects.get(pk=pk, status='normal')
    except model.DoesNotExist:
        return None

def update_model_data_by_pk(model, pk, data):
    model.objects.filter(pk=pk).update(**data)