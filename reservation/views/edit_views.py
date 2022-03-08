from django.shortcuts import render, get_object_or_404, redirect
from ..models import Reservation
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def myrange(start, end, step):
    r = start
    while (r<end):
        yield r
        r += step

@login_required
def new(request, equipment_type):

    # 요일 가져오기
    today = datetime.now() # 2021-03-27 01:27:32.470639 시간 있음
    today_day = today.weekday() # 무슨요일인지 파악. 월화수목금토일 0123456
    weekday_mark = 0

    # 평일과 주말 상관없이 모두 예약 가능
    start_day = today - timedelta(days=today_day)  # 이번주 시작 월요일
    start_day_prev = today - timedelta(days=today_day) - timedelta(weeks=1) # 저번주 시작 월요일
    start_day_next = today - timedelta(days=today_day) + timedelta(weeks=1) # 다음주 시작 월요일
    start_day_diff = 0 - today_day  # 0 - 오늘요일 차이 # 다름

    date_diff = 13-today_day # 마지막 날짜, 그다음주 금요일까지

    # 현재 예약 상황 넘겨 주기
    reservations = Reservation.objects.all()


    #  월~일 예약된 장비 목록 보여주기

    #  이번주
    day_list = []
    name_list = []
    for i in range(0,7): # 토, 일 5, 6
        day = start_day + timedelta(days=i)
        reservations_day = reservations.filter( # 하루치 예약 목록, 사람 구별 없음
            equipment_type=equipment_type,
            # author__username=request.user.username,
            equipment_date=day
        ).order_by('equip_start_time')
        temp_list = [] # 예약 시작 시간, 예약 끝 시간, 간격(30분) # 하루치
        user_list = []
        for res in reservations_day:
            temp_list.extend(myrange(res.equip_start_time, res.equip_finish_time, 0.5))
            for _ in myrange(res.equip_start_time,res.equip_finish_time, 0.5):
                user_list.append(res.author.username)
                from accounts.models import Profile
                profile = Profile.objects.filter(user=res.author)
                # print(res.author)
                print(profile)
                # print(profile.realname)
        day_list.append(temp_list) # 일주일치
        name_list.append(user_list)

    # 저번주
    day_list_prev = []
    name_list_prev = []
    for i in range(0,7): # 토, 일 5, 6
        # day_prev = start_day + timedelta(days=i) - timedelta(days=11)
        day_prev = start_day_prev + timedelta(days=i)
        reservations_day_prev = reservations.filter( # 하루치 예약 목록
            equipment_type=equipment_type,
            # author__username=request.user.username,
            equipment_date=day_prev
        ).order_by('equip_start_time')
        temp_list_prev = [] # 예약 시작 시간, 예약 끝 시간, 간격(30분)
        user_list_prev = []
        for res_prev in reservations_day_prev:
            temp_list_prev.extend(myrange(res_prev.equip_start_time, res_prev.equip_finish_time, 0.5))
            for _ in myrange(res_prev.equip_start_time,res_prev.equip_finish_time, 0.5):
                user_list_prev.append(res_prev.author.username)
        day_list_prev.append(temp_list_prev)
        name_list_prev.append(user_list_prev)

    # 다음주
    day_list_next = []
    name_list_next = []
    for i in range(0, 7):  # 토, 일 5, 6
        # day_next = start_day + timedelta(days=i) + timedelta(days=9)
        day_next = start_day_next + timedelta(days=i)
        reservations_day_next = reservations.filter(  # 하루치 예약 목록
            equipment_type=equipment_type,
            # author__username=request.user.username,
            equipment_date=day_next
        ).order_by('equip_start_time')
        user_list_next = []
        temp_list_next = []  # 예약 시작 시간, 예약 끝 시간, 간격(30분)
        for res_next in reservations_day_next:
            temp_list_next.extend(myrange(res_next.equip_start_time, res_next.equip_finish_time, 0.5))
            for _ in myrange(res_next.equip_start_time,res_next.equip_finish_time, 0.5):
                user_list_next.append(res_next.author.username)
        day_list_next.append(temp_list_next)
        name_list_next.append(user_list_next)

    if 'Chiller' in equipment_type:
        return render(request, 'reservation/new_chiller.html', {
            'author_username': request.user.username,
            'equipment_type': equipment_type,
            'date_diff': date_diff,
            'weekday_mark': weekday_mark,
            'day_list': day_list,
            'start_day_diff': start_day_diff,
            'name_list': name_list,

            # prev
            'day_list_prev': day_list_prev,
            'name_list_prev': name_list_prev,
            # next
            'day_list_next': day_list_next,
            'name_list_next': name_list_next,
        })
    else:
        return render(request, 'reservation/new.html', {
            'author_username': request.user.username,
            'equipment_type': equipment_type,
            'date_diff':date_diff,
            'weekday_mark':weekday_mark,
            'day_list':day_list,
            'start_day_diff':start_day_diff,
            'name_list': name_list,

            # prev
            'day_list_prev': day_list_prev,
            'name_list_prev': name_list_prev,
            # next
            'day_list_next': day_list_next,
            'name_list_next': name_list_next,
        })

@login_required
def new_hood(request, yoil):

    Hood_list=['Hood_1_1', 'Hood_1_2', 'Hood_1_3', 'Hood_1_4',
                    'Hood_2_1', 'Hood_2_2', 'Hood_2_3', 'Hood_2_4',
                    'Hood_3_1', 'Hood_3_2', 'Hood_3_3', 'Hood_3_4']
    # 요일 가져오기
    today = datetime.now() # 2021-03-27 01:27:32.470639 시간 있음
    today_day = today.weekday() # 무슨요일인지 파악. 월화수목금토일 0123456
    weekday_mark = 0

    # 평일과 주말 상관없이 모두 예약 가능
    start_day = today - timedelta(days=today_day)  # 이번주 시작 월요일
    start_day_prev = today - timedelta(days=today_day) - timedelta(weeks=1) # 저번주 시작 월요일
    start_day_next = today - timedelta(days=today_day) + timedelta(weeks=1) # 다음주 시작 월요일
    start_day_diff = 0 - today_day  # 0 - 오늘요일 차이 # 다름

    date_diff = 13-today_day # 마지막 날짜, 그다음주 금요일까지

    # 현재 예약 상황 넘겨 주기
    reservations = Reservation.objects.all()


    #  월~일 예약된 장비 목록 보여주기
    day_list = []
    name_list = []
    for hood in Hood_list:
        reservations_day = reservations.filter( # 핫플레이트 1개의 예약 목록
            equipment_type=hood,
            equipment_date=start_day + timedelta(days=yoil)
        ).order_by('equip_start_time')
        temp_list = [] # 예약 시작 시간, 예약 끝 시간, 간격(30분)
        user_list = []
        for res in reservations_day:
            temp_list.extend(myrange(res.equip_start_time, res.equip_finish_time, 0.5))
            for _ in myrange(res.equip_start_time, res.equip_finish_time, 0.5):
                user_list.append(res.author.username)
        day_list.append(temp_list)
        name_list.append(user_list)

    # 저번주
    day_list_prev = []
    name_list_prev = []
    for hood in Hood_list:
        reservations_day_prev = reservations.filter( # 하루치 예약 목록
            equipment_type=hood,
            equipment_date=start_day_prev + timedelta(days=yoil)
        ).order_by('equip_start_time')
        temp_list_prev = [] # 예약 시작 시간, 예약 끝 시간, 간격(30분)
        user_list_prev = []
        for res_prev in reservations_day_prev:
            temp_list_prev.extend(myrange(res_prev.equip_start_time, res_prev.equip_finish_time, 0.5))
            for _ in myrange(res_prev.equip_start_time, res_prev.equip_finish_time, 0.5):
                user_list_prev.append(res_prev.author.username)
        day_list_prev.append(temp_list_prev)
        name_list_prev.append(user_list_prev)

    # 다음주
    day_list_next = []
    name_list_next = []
    for hood in Hood_list:
        reservations_day_next = reservations.filter(  # 하루치 예약 목록
            equipment_type=hood,
            equipment_date=start_day_next + timedelta(days=yoil)
        ).order_by('equip_start_time')
        temp_list_next = []  # 예약 시작 시간, 예약 끝 시간, 간격(30분)
        user_list_next = []
        for res_next in reservations_day_next:
            temp_list_next.extend(myrange(res_next.equip_start_time, res_next.equip_finish_time, 0.5))
            for _ in myrange(res_next.equip_start_time, res_next.equip_finish_time, 0.5):
                user_list_next.append(res_next.author.username)
        day_list_next.append(temp_list_next)
        name_list_next.append(user_list_next)

    return render(request, 'reservation/new_hood.html', {
                                                    'author_username': request.user.username,
                                                    'date_diff':date_diff,
                                                    'weekday_mark':weekday_mark,
                                                    'day_list':day_list,
                                                    'start_day_diff':start_day_diff,
                                                    'name_list': name_list,

                                                    # prev
                                                    'day_list_prev': day_list_prev,
                                                    'name_list_prev': name_list_prev,
                                                    # next
                                                    'day_list_next': day_list_next,
                                                    'name_list_next': name_list_next,
                                                    'yoil': yoil,
                                                    })

def delete(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    if reservation.author == request.user:
        reservation.delete()
    return redirect('/reservation/my')