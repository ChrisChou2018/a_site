`将数据库数据导出保存为json数据`
执行命令
```
# 导出 column_manage app下的models中所有的数据
python manage.py dumpdata --format=json column_manage > ubskin_site/column_manage/fixtures/columns_data.json
# 导入item column_manage 数据
python manage.py loaddata columns_data.json

# 导出 extends_manage app下的models中所有的数据
python manage.py dumpdata --format=json extends_manage > ubskin_site/extends_manage/fixtures/extends_data.json
# extends_manage app 数据
python manage.py loaddata extends_data.json



# 将数据库清空的命令
python manage.py flush

```