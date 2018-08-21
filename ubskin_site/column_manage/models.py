import time

from django.db import models
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models import Count



class Columns(models.Model):
    '''
    菜单栏表
    '''
    columns_id = models.AutoField(db_column="columns_id", primary_key=True, verbose_name="菜单栏ID")
    column_name = models.CharField(db_column="column_name", verbose_name="菜单栏名称", max_length=255)
    type_choises = (
        (1, '导航栏目'),
        (2, '单网页'),
        (3, '菜单'),
    )
    columns_type = models.SmallIntegerField(choices=type_choises, db_column='columns_type', verbose_name='菜单类型')
    link = models.CharField(db_column="link", verbose_name="链接地址", max_length=1000, null=True, blank=True)
    photo_id = models.CharField(db_column="photo_id", null=True, blank=True, verbose_name='图片ID', max_length=255)
    thumb_photo_id = models.CharField(db_column="thumb_photo_id", null=True, blank=True, verbose_name='小图片ID', max_length=255)
    parent_id = models.BigIntegerField(db_column='parent_id', verbose_name='父级菜单ID', null=True, blank=True,)
    page_type_choices = (
        (1, '文本图片'),
        (2, '留言页面'),
        (3, '店铺查询页面'),
        (4, '文章列表类型页面'),
        (5, '重点店铺页面'),
    )
    page_type = models.SmallIntegerField(choices=page_type_choices, db_column='page_type', verbose_name='单页面类型', null=True, blank=True)
    has_scrolling_image = models.BooleanField(db_column="has_scrolling_image", verbose_name="是否有轮播图", default=False)
    status = models.CharField(db_column="status", verbose_name="数据状态", default="normal", max_length=255)


    class Meta:
        db_table = 'columns'
    
    @classmethod
    def get_all_select_columns(cls, self_id=None, is_chld_column=False):
        column_index_list = cls.objects.filter(columns_type=1,status='normal').values('columns_id', 'column_name')
        for i in column_index_list:
            if self_id:
                child = cls.objects.filter(~Q(columns_id=self_id), parent_id=i['columns_id'], status='normal', columns_type=3).values('columns_id', 'column_name')
            else:
                child = cls.objects.filter(parent_id=i['columns_id'], status='normal', columns_type=3).values('columns_id', 'column_name')
            if child and not is_chld_column:
                for j in child:
                    j['column_name'] = i['column_name'] + '__' + j['column_name']
                i['child'] = child
        if column_index_list:
            return column_index_list
        else:
            return list()
    
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
        find_all_child(data_id, id_list)
        cls.objects.filter(pk__in=id_list).update(status='deleted')
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


class Article(models.Model):

    article_id  = models.AutoField(db_column="article_id", primary_key=True, verbose_name="文章ID")
    columns_id = models.BigIntegerField(db_column="columns_id", verbose_name="所属栏目ID", null=True, blank=True)
    article_type_choices = (
        (1, '普通文章类型'),
        (2, '突出图片标题'),
    )
    article_type = models.SmallIntegerField(db_column='article_type', verbose_name='文章列表类型', default=1)
    article_title = models.CharField(db_column="article_title", verbose_name="文章标题", max_length=255, null=True, blank=True)
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