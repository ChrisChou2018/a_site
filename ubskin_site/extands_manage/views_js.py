
from django.http import JsonResponse

from ubskin_site.extands_manage import models as extands_models



def delete_team(request):
    if request.method == "POST":
        data_id_list = request.POST.getlist('data_id_list[]')
        for i in data_id_list:
            extands_models.update_model_data_by_pk(
                extands_models.TeamWork,
                i,
                {'status': 'deleted'}
            )
        return JsonResponse({'status': 'success'})