from ..models import Reservation
from django.http import HttpResponse
import json
from datetime import datetime

# ajax
def check(request):
    equipment_type_vr = request.POST.get('equipment_type', None)
    equipment_date_vr = request.POST.get('equipment_date', None)  # ajax 통신으로 template에서 POST방식으로 전달
    equip_start_time_vr = request.POST.get('equip_start_time', None)
    equip_finish_time_vr = request.POST.get('equip_finish_time', None)

    reservations = Reservation.objects.all()
    reserve_date = datetime.strptime(equipment_date_vr, "%Y-%m-%d ").date()
    check_error = 0 # 정상

    # 겹치는 시간 있는지 체크
    message = "이미 예약된 시간입니다."

    if reservations.filter(equipment_type=equipment_type_vr, equipment_date=reserve_date, equip_finish_time__gt=equip_start_time_vr, equip_start_time__lt=equip_finish_time_vr).count() != 0:
        check_error = 1
        context = {
            "message":message,
            'check_error':check_error
        }
        return HttpResponse(json.dumps(context), content_type="application/json")
    if reservations.filter(equipment_type=equipment_type_vr, equipment_date=reserve_date, equip_finish_time__lt=equip_finish_time_vr, equip_start_time__gt=equip_start_time_vr).count() != 0:
        check_error = 1
        context = {
            "message":message,
            'check_error':check_error
        }
        return HttpResponse(json.dumps(context), content_type="application/json")

    context = {
        'message':message,
        'check_error':check_error
    }
    return HttpResponse(json.dumps(context), content_type="application/json")