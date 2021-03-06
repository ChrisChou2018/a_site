# Generated by Django 2.0.6 on 2018-08-13 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('column_manage', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='columns',
            name='parent_id',
            field=models.BigIntegerField(blank=True, db_column='parent_id', null=True, verbose_name='父级菜单ID'),
        ),
        migrations.AlterField(
            model_name='article',
            name='create_time',
            field=models.IntegerField(db_column='create_time', default=1534153595, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='columns',
            name='columns_type',
            field=models.SmallIntegerField(choices=[(1, '页面链接'), (2, '单网页'), (3, '菜单'), (4, '文章类型')], db_column='columns_type', verbose_name='菜单类型'),
        ),
    ]
