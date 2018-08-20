from django.shortcuts import render

# Create your views here.

def my_render(request, templater_path, **kwargs):
    return render(request, templater_path, dict(**kwargs))

def extands_manage(request):
    if request.method == "GET":
        return my_render(
            request,
            'column_manage/extands_manage.html'
        )