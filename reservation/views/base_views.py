from django.shortcuts import render
from ..models import Reservation, Blog
from datetime import datetime

def home(request):
    today =  datetime.now()
    equip_Hood = Reservation.objects.filter(equipment_date = today, equipment_type ='Hood')
    equip_Chiller = Reservation.objects.filter(equipment_date = today, equipment_type ='Chiller')
    equip_Press = Reservation.objects.filter(equipment_date = today, equipment_type ='Press')
    equip_Dsc = Reservation.objects.filter(equipment_date = today, equipment_type ='Press')
    equip_Gpc = Reservation.objects.filter(equipment_date = today, equipment_type ='Dsc')
    equip_Utm = Reservation.objects.filter(equipment_date = today, equipment_type ='Gpc')
    equip_Crosslinker = Reservation.objects.filter(equipment_date = today, equipment_type ='Crosslinker')
    proportion = [0,0,0,0,0,0,0]
    for r in equip_Hood:
        proportion[0] += (r.equip_finish_time - r.equip_start_time)
    for r in equip_Chiller:
        proportion[1] += (r.equip_finish_time - r.equip_start_time)
    for r in equip_Press:
        proportion[2] += (r.equip_finish_time - r.equip_start_time)
    for r in equip_Dsc:
        proportion[3] += (r.equip_finish_time - r.equip_start_time)
    for r in equip_Gpc:
        proportion[4] += (r.equip_finish_time - r.equip_start_time)
    for r in equip_Utm:
        proportion[5] += (r.equip_finish_time - r.equip_start_time)
    for r in equip_Crosslinker:
        proportion[6] += (r.equip_finish_time - r.equip_start_time)


    notice_list = Blog.objects.filter(category="공지사항").order_by('-created') # 공지사항
    notices = notice_list[0:3]

    lost_list = Blog.objects.filter(category="분실물").order_by('-created') # 공지사항
    losts = lost_list[0:3]

    return render(request, 'reservation/home.html', {'notices':notices, 'losts':losts,  'proportion':proportion})