
from django.http import JsonResponse

from ubskin_site.extends_manage import models as extends_models



def delete_team(request):
    if request.method == "POST":
        data_id_list = request.POST.getlist('data_id_list[]')
        for i in data_id_list:
            extends_models.update_model_data_by_pk(
                extends_models.TeamWork,
                i,
                {'status': 'deleted'}
            )
        return JsonResponse({'status': 'success'})