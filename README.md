`将数据库数据导出保存为json数据`
执行命令
```

# 导入item column_manage 数据
python manage.py loaddata columns_data.json


# extends_manage app 数据
python manage.py loaddata extends_data.json



# 将数据库清空的命令
python manage.py flush

```