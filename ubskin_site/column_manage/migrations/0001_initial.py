# Generated by Django 2.0.6 on 2018-08-13 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('article_id', models.AutoField(db_column='article_id', primary_key=True, serialize=False, verbose_name='文章ID')),
                ('article_title', models.CharField(db_column='article_title', max_length=255, verbose_name='文章标题')),
                ('article_content', models.TextField(db_column='article_content', verbose_name='文章内容')),
                ('status', models.CharField(db_column='status', default='normal', max_length=255, verbose_name='数据状态')),
                ('photo_id', models.CharField(blank=True, db_column='photo_id', max_length=255, null=True, verbose_name='图片ID')),
                ('create_time', models.IntegerField(db_column='create_time', default=1534150665, verbose_name='创建时间')),
            ],
            options={
                'db_table': 'article',
            },
        ),
        migrations.CreateModel(
            name='Columns',
            fields=[
                ('columns_id', models.AutoField(db_column='columns_id', primary_key=True, serialize=False, verbose_name='菜单栏ID')),
                ('column_name', models.CharField(db_column='column_name', max_length=255, verbose_name='菜单栏名称')),
                ('columns_type', models.SmallIntegerField(choices=[(1, '页面链接'), (2, '网页'), (3, '菜单'), (4, '文章类型')], db_column='columns_type')),
                ('link', models.CharField(db_column='link', max_length=1000, verbose_name='链接地址')),
                ('photo_id', models.CharField(blank=True, db_column='photo_id', max_length=255, null=True, verbose_name='图片ID')),
                ('status', models.CharField(db_column='status', default='normal', max_length=255, verbose_name='数据状态')),
            ],
            options={
                'db_table': 'columns',
            },
        ),
    ]
