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