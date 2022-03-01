from django.shortcuts import render, redirect, get_object_or_404
from ..models import Reservation
from django.utils import timezone
from datetime import datetime, date, timedelta
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create
@login_required
def create(request):

    reserve_date = datetime.strptime(request.GET.get('equipment_date'), "%Y-%m-%d ").date() # strptime: 문자열을 datetime으로 변환

    # 만들기
    reservation = Reservation() # 객체 만들기
    reservation.author = request.user # 내용 채우기
    reservation.equipment_type = request.GET.get('equipment_type') # 내용 채우기
    reservation.equipment_date = reserve_date # 내용 채우기

    # 시간 구하기
    reservation.equip_start_time = request.GET.get('equip_start_time')
    reservation.equip_finish_time = request.GET.get('equip_finish_time')
    reservation.created = timezone.datetime.now() # 내용 채우기
    reservation.save() # 객체 저장하기

    # 내 예약 주소
    return redirect('/reservation/my')

def myreservation(request):
    # myreserv = get_object_or_404(Reservation, pk=request.user.username)
    today = date.today() # 오늘 날짜
    now_time = datetime.now() # ex) (2007, 12, 6, 16, 29, 43, 79043)
    now = now_time.hour + (now_time.minute/60) # 현재 시간 # 왜 60으로나누는거지?
    reservations = Reservation.objects.filter(author__username=request.user.username)
    # 장비 예약 날짜가 오늘보다 크거나 끝나는시간이 지금보다 나중일때 목록을 불러옴
    # reservation_list = reservations.filter(Q(author=request.user.username, equipment_date__gt=today)|Q(author=request.user.username, equipment_date=today, equip_finish_time__gte=now))
    # reservation_list = Reservation.objects.filter(Q(user=request.user.username, equipment_date__gt=today)|Q(user=request.user.username, equipment_date=today, equip_finish_time__gte=now))
    reservation_list = reservations.filter(Q(equipment_date__gt=today)|Q(equipment_date=today, equip_finish_time__gte=now))
    return  render(request, 'reservation/myreservation.html', {'reservation_list':reservation_list})


def myrange(start, end, step):
    r = start
    while (r<end):
        yield r
        r += step

@login_required
def total(request, equipment_type):

    # 요일 가져오기
    today = datetime.now() # 2021-03-27 01:27:32.470639 시간 있음
    today_day = today.weekday() # 무슨요일인지 파악. 월화수목금토일 0123456
    weekday_mark = 0

    # 평일과 주말 상관없이 모두 예약 가능
    start_day = today - timedelta(days=today_day)  # 이번주 시작 월요일
    start_day_prev = today - timedelta(days=today_day) - timedelta(weeks=1) # 저번주 시작 월요일
    start_day_next = today - timedelta(days=today_day) + timedelta(weeks=1) # 다음주 시작 월요일
    start_day_diff = 0 - today_day  # 0 - 오늘요일 차이 # 다름

    # date_diff = 4-today_day # 마지막 날짜
    date_diff = 13-today_day # 마지막 날짜, 그다음주 금요일까지

    # 현재 예약 상황 넘겨 주기
    reservations = Reservation.objects.all()
    day_list = []

    #  월~일 예약된 장비 목록 보여주기
    #  이번주
    for i in range(0,7): # 토, 일 5, 6
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

    # 저번주
    day_list_prev = []
    for i in range(0,7): # 토, 일 5, 6
        # day_prev = start_day + timedelta(days=i) - timedelta(days=11)
        day_prev = start_day_prev + timedelta(days=i)
        reservations_day_prev = reservations.filter( # 하루치 예약 목록
            equipment_type=equipment_type,
            author__username=request.user.username,
            equipment_date=day_prev
        ).order_by('equip_start_time')
        temp_list_prev = [] # 예약 시작 시간, 예약 끝 시간, 간격(30분)
        for res_prev in reservations_day_prev:
            temp_list_prev.extend(myrange(res_prev.equip_start_time, res_prev.equip_finish_time, 0.5))
        day_list_prev.append(temp_list_prev)

    # 다음주
    day_list_next = []
    for i in range(0, 7):  # 토, 일 5, 6
        # day_next = start_day + timedelta(days=i) + timedelta(days=9)
        day_next = start_day_next + timedelta(days=i)
        reservations_day_next = reservations.filter(  # 하루치 예약 목록
            equipment_type=equipment_type,
            author__username=request.user.username,
            equipment_date=day_next
        ).order_by('equip_start_time')
        temp_list_next = []  # 예약 시작 시간, 예약 끝 시간, 간격(30분)
        for res_next in reservations_day_next:
            temp_list_next.extend(myrange(res_next.equip_start_time, res_next.equip_finish_time, 0.5))
        day_list_next.append(temp_list_next)

    return render(request, 'reservation/total.html', {
                                                'author_username': request.user.username,
                                                'equipment_type': equipment_type,
                                                'date_diff':date_diff,
                                                'weekday_mark':weekday_mark,
                                                'day_list':day_list,
                                                'start_day_diff':start_day_diff,

                                                # prev
                                                'day_list_prev': day_list_prev,
                                                # next
                                                'day_list_next': day_list_next,
                                                })