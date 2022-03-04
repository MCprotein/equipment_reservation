from django.shortcuts import render
from ..models import Reservation, Blog
from datetime import datetime

def home(request):
    today =  datetime.now()
    equip_Hood_1_1 = Reservation.objects.filter(equipment_date = today, equipment_type ='Hood_1_1')
    equip_Hood_1_2 = Reservation.objects.filter(equipment_date = today, equipment_type ='Hood_1_2')
    equip_Hood_1_3 = Reservation.objects.filter(equipment_date = today, equipment_type ='Hood_1_3')
    equip_Hood_1_4 = Reservation.objects.filter(equipment_date = today, equipment_type ='Hood_1_4')
    equip_Hood_2_1 = Reservation.objects.filter(equipment_date = today, equipment_type ='Hood_2_1')
    equip_Hood_2_2 = Reservation.objects.filter(equipment_date = today, equipment_type ='Hood_2_2')
    equip_Hood_2_3 = Reservation.objects.filter(equipment_date = today, equipment_type ='Hood_2_3')
    equip_Hood_2_4 = Reservation.objects.filter(equipment_date = today, equipment_type ='Hood_2_4')
    equip_Hood_3_1 = Reservation.objects.filter(equipment_date = today, equipment_type ='Hood_3_1')
    equip_Hood_3_2 = Reservation.objects.filter(equipment_date = today, equipment_type ='Hood_3_2')
    equip_Hood_3_3 = Reservation.objects.filter(equipment_date = today, equipment_type ='Hood_3_3')
    equip_Hood_3_4 = Reservation.objects.filter(equipment_date = today, equipment_type ='Hood_3_4')
    equip_Chiller_D = Reservation.objects.filter(equipment_date = today, equipment_type ='Chiller_D') # 칠러_대한과학
    equip_Chiller_J = Reservation.objects.filter(equipment_date = today, equipment_type ='Chiller_J') # 칠러_제이오텍
    equip_Press = Reservation.objects.filter(equipment_date = today, equipment_type ='Press')
    equip_Dsc = Reservation.objects.filter(equipment_date = today, equipment_type ='Dsc')
    equip_Gpc = Reservation.objects.filter(equipment_date = today, equipment_type ='Gpc')
    equip_Utm = Reservation.objects.filter(equipment_date = today, equipment_type ='Utm')
    equip_Crosslinker = Reservation.objects.filter(equipment_date = today, equipment_type ='Crosslinker')
    proportion = [0,0,0,0,0,0,0]
    for r in equip_Hood_1_1:
        proportion[0] += (r.equip_finish_time - r.equip_start_time)/12
    for r in equip_Hood_1_2:
        proportion[0] += (r.equip_finish_time - r.equip_start_time)/12
    for r in equip_Hood_1_3:
        proportion[0] += (r.equip_finish_time - r.equip_start_time)/12
    for r in equip_Hood_1_4:
        proportion[0] += (r.equip_finish_time - r.equip_start_time)/12
    for r in equip_Hood_2_1:
        proportion[0] += (r.equip_finish_time - r.equip_start_time)/12
    for r in equip_Hood_2_2:
        proportion[0] += (r.equip_finish_time - r.equip_start_time)/12
    for r in equip_Hood_2_3:
        proportion[0] += (r.equip_finish_time - r.equip_start_time)/12
    for r in equip_Hood_2_4:
        proportion[0] += (r.equip_finish_time - r.equip_start_time)/12
    for r in equip_Hood_3_1:
        proportion[0] += (r.equip_finish_time - r.equip_start_time)/12
    for r in equip_Hood_3_2:
        proportion[0] += (r.equip_finish_time - r.equip_start_time)/12
    for r in equip_Hood_3_3:
        proportion[0] += (r.equip_finish_time - r.equip_start_time)/12
    for r in equip_Hood_3_4:
        proportion[0] += (r.equip_finish_time - r.equip_start_time)/12
    for r in equip_Chiller_D:
        proportion[1] += (r.equip_finish_time - r.equip_start_time)/2
    for r in equip_Chiller_J:
        proportion[1] += (r.equip_finish_time - r.equip_start_time)/2
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