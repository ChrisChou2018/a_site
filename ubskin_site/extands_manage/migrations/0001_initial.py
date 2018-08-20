# Generated by Django 2.0.6 on 2018-08-20 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TeamWork',
            fields=[
                ('team_work_id', models.AutoField(db_column='team_work_id', primary_key=True, serialize=False, verbose_name='合作商ID')),
                ('team_name', models.CharField(blank=True, db_column='team_name', max_length=255, null=True, verbose_name='合作商名称')),
                ('team_link', models.CharField(db_column='team_link', default='#a', max_length=255, verbose_name='合作商链接')),
                ('phtot_id', models.CharField(blank=True, db_column='photo_id', max_length=255, null=True, verbose_name='合作商logo')),
                ('team_type', models.SmallIntegerField(blank=True, db_column='team_type', null=True, verbose_name='合作商类型')),
                ('is_show', models.BooleanField(db_column='is_show', default=True, verbose_name='是否展示')),
                ('status', models.CharField(db_column='status', default='normal', max_length=255, verbose_name='数据状态')),
            ],
            options={
                'db_table': 'team_work',
            },
        ),
    ]