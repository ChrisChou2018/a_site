# Generated by Django 2.0.6 on 2018-08-14 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member_manage', '0002_auto_20180813_1746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='create_time',
            field=models.IntegerField(db_column='create_time', default=1534234344),
        ),
        migrations.AlterField(
            model_name='member',
            name='update_time',
            field=models.IntegerField(db_column='update_time', default=1534234344),
        ),
    ]
