from django.shortcuts import render, get_object_or_404, redirect
from ..models import Reservation
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required

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
    # if today_day < 5:
    #     start_day = today - timedelta(days=today_day) # 시작 월요일
    #     start_day_diff = 0 - today_day # 0 - 오늘요일 차이 # 다름

    # 주말 -> 다음주, 다다음주까지 예약 가능
    # elif today_day >= 5:
    #     start_day_diff = 7- today_day
    #     weekday_mark = 7- today_day
    #     start_day = today + timedelta(weekday_mark)

    # 평일과 주말 상관없이 모두 예약 가능
    start_day = today - timedelta(days=today_day)  # 시작 월요일
    start_day_diff = 0 - today_day  # 0 - 오늘요일 차이 # 다름

    # date_diff = 4-today_day # 마지막 날짜
    date_diff = 13-today_day # 마지막 날짜, 그다음주 금요일까지

    # 현재 예약 상황 넘겨 주기
    reservations = Reservation.objects.all()
    day_list = []

    #  월~금 예약된 장비 목록 보여주기
    for i in range(0,5):
        day = start_day + timedelta(days=i)
        reservations_day = reservations.filter( # 하루치 예약 목록
            equipment_type=equipment_type,
            author__username=request.user.username,
            equipment_date=day
        ).order_by('equip_start_time')
        temp_list = [] # 예약 시작 시간, 예약 끝 시간, 간격(30분)
        for res in reservations_day:
            temp_list.extend(myrange(res.equip_start_time, res.equip_finish_time, 0.5))
        day_list.append(temp_list)
    return render(request, 'reservation/new.html', {
                                                'author_username': request.user.username,
                                                'equipment_type': equipment_type,
                                                'date_diff':date_diff,
                                                'weekday_mark':weekday_mark,
                                                'day_list':day_list,
                                                'start_day_diff':start_day_diff
                                                })

def edit(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    min_date = datetime.now().strftime("%Y-%m-%d") # 오늘부터
    max_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d") # 14일 후까지 가능
    return render(request, 'reservation/edit.html', {'reservation':reservation, 'min_date':min_date, 'max_date':max_date})

def update(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    reservation.equipment_type = request.GET.get('equipment_type')
    reservation.equipment_date = request.GET.get('equipment_date')
    reservation.equip_start_time = request.GET.get('equip_start_time')
    reservation.equip_finish_time = request.GET.get('equip_finish_time')
    reservation.save()

    return redirect('/reservation/'+str(reservation.id)) # 새로운 예약 url 주소로 이동

def delete(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    if reservation.author == request.user:
        reservation.delete()
    return redirect('/reservation/my')