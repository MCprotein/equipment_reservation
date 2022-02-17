from django.shortcuts import render, get_object_or_404, redirect
from .models import Reservation, Blog
from django.utils import timezone
from datetime import datetime, timedelta, date
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import json, time
from django.db.models import Q

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
        proportion[0] += (r.eqiup_finish_time - r.equip_start_time)
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


# library funciton

def myrange(start, end, step):
    r = start
    while (r<end):
        yield r
        r += step

@login_required
def new(request, equipment_type):

    # 요일 가져오기
    today = datetime.now() # 2021-03-27 01:27:32.470639 시간 있음
    today_day = today.weekday() # 5 시간 없음
    weekday_mark = 0

    # 평일
    if today_day < 5:
        start_day = today - timedelta(days=today_day) # 시작 월요일
        start_day_diff = 0 - today_day # 0 - 오늘요일 차이 # 다름

    # 주말 -> 다음주, 다다음주까지 예약 가능
    elif today_day >= 5:
        start_day_diff = 7- today_day
        weekday_mark = 7- today_day
        start_day = today + timedelta(weekday_mark)
    date_diff = 4-today_day # 마지막 날짜 이게뭐지?

    # 현재 예약 상황 넘겨 주기
    reservations = Reservation.objects.all()
    day_list = []

    #  월~금 예약된 장비 목록 보여주기
    for i in range(0,5):
        day = start_day + timedelta(days=i)
        reservations_day = reservations.filter( # 하루치 예약 목록
            equipment_type=equipment_type,
            user=request.user.username,
            equipment_date=day
        ).order_by('equip_start_time')
        temp_list = [] # 예약 시작 시간, 예약 끝 시간, 간격(30분)
        for res in reservations_day:
            temp_list.extend(myrange(res.equip_start_time, res.equip_finish_time, 0.5))
        day_list.append(temp_list)
    return render(request, 'reservation/new.html', {
                                                'equipment_type': equipment_type,
                                                'date_diff':date_diff,
                                                'weekday_mark':weekday_mark,
                                                'day_list':day_list,
                                                'start_day_diff':start_day_diff
                                                })