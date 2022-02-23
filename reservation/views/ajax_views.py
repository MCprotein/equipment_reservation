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

    # 고쳐봐야겠음 왜 if로 하지 ?
    # <1> 오른쪽 겹치기
    # start 시간보다 크고 finish 시간보다 작다
    if reservations.filter(equipment_type=equipment_type_vr, equipment_date=reserve_date, equip_finish_time__gt=equip_start_time_vr, equip_start_time__lt=equip_finish_time_vr).count() != 0:
        check_error = 1
        context = {
            "message":message,
            'check_error':check_error
        }
        return HttpResponse(json.dumps(context), content_type="application/json")
    # <2> 사이 들어가기
    # start 시간보다 작거나 같고 finish 시간보다 크거나 같다
    if reservations.filter(equipment_type=equipment_type_vr, equipment_date=reserve_date, equip_finish_time__lte=equip_start_time_vr, equip_start_time__gte=equip_finish_time_vr).count() != 0:
        check_error = 1
        context = {
            "message":message,
            'check_error':check_error
        }
        return HttpResponse(json.dumps(context), content_type="application/json")
    # <3> 오른쪽 포개지기
    # start 시간보다 작고 finish 시간보다 크다
    if reservations.filter(equipment_type=equipment_type_vr, equipment_date=reserve_date, equip_finish_time__lt=equip_finish_time_vr, equip_start_time__gt=equip_start_time_vr).count() != 0:
        check_error = 1
        context = {
            "message":message,
            'check_error':check_error
        }
        return HttpResponse(json.dumps(context), content_type="application/json")
    # <4> 밖에 감싸기
    # start 시간보다 크거나 같고 finish 시간보다 작거나 같다
    if reservations.filter(equipment_type=equipment_type_vr, equipment_date=reserve_date, equip_finish_time__gte=equip_start_time_vr, equip_start_time__lte=equip_finish_time_vr).count() != 0:
        check_error = 1
        context = {
            "message":message,
            'check_error':check_error
        }
        return HttpResponse(json.dumps(context), content_type="application/json")
    # <5> 가능
    context = {
        'message':message,
        'check_error':check_error
    }
    return HttpResponse(json.dumps(context), content_type="application/json")