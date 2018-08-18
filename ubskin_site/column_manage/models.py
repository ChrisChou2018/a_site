import time

from django.db import models
from django.core.paginator import Paginator
from django.db.models import Q



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
        (3, '店铺查询'),
        (4, '文章列表类型'),
    )
    page_type = models.SmallIntegerField(choices=page_type_choices, db_column='page_type', verbose_name='单页面类型', null=True, blank=True)
    has_scrolling_image = models.BooleanField(db_column="has_scrolling_image", verbose_name="是否有轮播图", default=False)
    status = models.CharField(db_column="status", verbose_name="数据状态", default="normal", max_length=255)


    class Meta:
        db_table = 'columns'
    
    @classmethod
    def get_all_select_columns(cls, self_id=None):
        column_index_list = cls.objects.filter(columns_type=1,status='normal').values('columns_id', 'column_name')
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
            child_list = cls.objects.filter(status='normal', parent_id=parent_obj.columns_id).values()
            data_list = find_all_child(child_list)
            return data_list
        else:
            return list()
    
    @classmethod
    def get_prent_photo(cls, data_id):
        photo_dict = dict()
        parent_obj = cls.objects.filter(columns_id=data_id)
        photo_dict['photo_id'] = parent_obj.photo_id
        photo_dict['thumb_photo_id'] = parent_obj.thumb_photo_id
        return photo_dict


class Article(models.Model):

    article_id  = models.AutoField(db_column="article_id", primary_key=True, verbose_name="文章ID")
    columns_id = models.BigIntegerField(db_column="columns_id", verbose_name="所属栏目ID", null=True, blank=True)
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
    def get_article_list_by_columns_id(cls, columns_id):
        return cls.objects.filter(columns_id=columns_id, status='normal')

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
    status = models.CharField(db_column="status", verbose_name="状态", max_length=255)


class ShopManage(models.Model):
    pass


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