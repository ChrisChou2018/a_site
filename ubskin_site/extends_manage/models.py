import time

from django.db import models
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models import Count

# Create your models here.


class TeamWork(models.Model):
    team_work_id = models.AutoField(db_column="team_work_id", primary_key=True, verbose_name="合作商ID")
    team_name = models.CharField(db_column="team_name", null=True, blank=True, verbose_name='合作商名称', max_length=255)
    team_link = models.CharField(db_column="team_link", verbose_name='合作商链接', max_length=255, default='#a')
    photo_id = models.CharField(db_column="photo_id", null=True, blank=True, verbose_name='合作商logo', max_length=255)
    team_choices = (
        (1, '推荐品牌'),
        (2, '推荐商场'),
        (3, '品牌'),
        (4, '商场'),
    )
    team_type = models.SmallIntegerField(db_column='team_type', null=True, blank=True, verbose_name='合作商类型')
    is_show = models.BooleanField(db_column='is_show', verbose_name='是否展示', default=True)
    status = models.CharField(db_column="status", verbose_name="数据状态", default="normal", max_length=255)


    class Meta:
        db_table = 'team_work'
    

    @classmethod
    def get_style_table_head(cls):
        return dict(
            team_work_id = '合作商ID',
            team_name = '合作商名称',
            team_type = '合作商类型',
            more = '更多'
        )

    @classmethod
    def get_team_work_for_index(cls):
        data_dict = dict()
        brand_top = cls.objects.filter(status='normal', team_type=1).first()
        data_dict['brand_top'] = brand_top
        brand_list = cls.objects.filter(status='normal', team_type=3)[0:20]
        data_dict['brand_list'] = brand_list
        shop_top = cls.objects.filter(status='normal', team_type=2).first()
        data_dict['shop_top'] = shop_top
        shop_list = cls.objects.filter(status='normal', team_type=4)[0:20]
        data_dict['shop_list'] = shop_list
        return data_dict

class Ad(models.Model):
    ad_id = models.AutoField(db_column="team_work_id", primary_key=True, verbose_name="合作商ID")
    ad_name = models.CharField(db_column='ad_name', verbose_name='广告名称', max_length=255)
    ad_title = models.CharField(db_column='ad_title', verbose_name='广告标题', max_length=255)
    ad_e_title = models.CharField(db_column='ad_e_title', verbose_name='广告英文标题', max_length=255)
    ad_text = models.CharField(db_column='ad_text', verbose_name='广告文字说明', max_length=1000)
    columns_id = models.BigIntegerField(db_column='columns_id', verbose_name='设置跳转的页面', null=True, blank=True)
    link = models.CharField(db_column='link', verbose_name='自定义链接', max_length=255, default='#a')
    location_choices = (
        (1, '首页轮播图'),
        (3, '广告位a'),
        (4, '广告位b_left'),
        (5, '广告位b_center'),
        (6, '广告为b_right'),
    )
    location = models.SmallIntegerField(db_column='location', verbose_name='location')
    photo_id = models.CharField(db_column="photo_id", null=True, blank=True, verbose_name='广告图', max_length=255)
    status = models.CharField(db_column="status", verbose_name="数据状态", default="normal", max_length=255)


    class Meta:
        db_table = 'ad'


    @classmethod
    def get_style_table_head(cls):
        return dict(
            ad_id = '广告ID',
            ad_name = '广告名',
            location = '广告位置',
            more = '更多',
        )
    
    @classmethod
    def get_ad_dict_for_page(cls):
        data_dict = dict()
        for i in cls.location_choices:
            data = cls.objects.filter(location=i[0], status='normal').values().order_by('pk')
            if i == 3:
                data = data[:4]
            elif i == 5:
                data = data[:3]
            if data:
                data_dict[i[0]] = data
        return data_dict

class Message(models.Model):
    message_id = models.AutoField(db_column="message_id", primary_key=True, verbose_name="留言ID")
    user_name = models.CharField(db_column="user_name", verbose_name="留言折姓名", max_length=255)
    gender = models.CharField(db_column="gender", verbose_name="性别", max_length=255)
    phone_number = models.CharField(db_column="phone_number", verbose_name="手机号码", max_length=255, null=True, blank=True)
    message_text = models.TextField(db_column="message_text", verbose_name="留言文本", null=True, blank=True)
    user_ip = models.CharField(db_column="user_ip", verbose_name="用户IP地址", max_length=255, null=True, blank=True)
    create_time = models.IntegerField(db_column='create_time', verbose_name='留言时间', default=int(time.time()))
    status = models.CharField(db_column="status", verbose_name="数据状态", default="normal", max_length=255)

    class Meta:
        db_table = 'message'
    

    @classmethod
    def get_style_table_head(cls):
        return dict(
            message_id = '留言ID',
            user_name = '姓名',
            message_text = '内容',
            gender = '性别',
            phone_number = '联系电话',
            create_time = '留言时间',
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