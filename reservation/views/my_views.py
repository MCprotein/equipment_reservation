from django.shortcuts import render, redirect
from ..models import Reservation
from django.utils import timezone
from datetime import datetime, date
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create
@login_required
def create(request):
    reserve_date = datetime.strptime(request.GET['equipment_date'], "%Y-%m%d ").date() # strptime: 문자열을 datetime으로 변환

    # 만들기
    reservation = Reservation() # 객체 만들기
    reservation.user = request.GET['user'] # 내용 채우기
    reservation.equipment_type = request.GET['equipment_type'] # 내용 채우기
    reservation.equip_date = reserve_date # 내용 채우기

    # 시간 구하기
    reservation.equip_start_time = request.GET['equip_start_time']
    reservation.equip_finish_time = request.GET['equip_finish_time']
    reservation.created = timezone.datetime.now() # 내용 채우기
    reservation.save() # 객체 저장하기

    # 내 예약 주소
    return redirect('/reservation/my')

def myreservation(request):
    today = date.today() # 오늘 날짜
    now_time = datetime.now() # ex) (2007, 12, 6, 16, 29, 43, 79043)
    now = now_time.hour + (now_time.minute/60) # 현재 시간 # 왜 60으로나누는거지?
    reservations = Reservation.objects.all()
    # 장비 예약 날짜가 오늘보다 크거나 끝나는시간이 지금보다 나중일때 목록을 불러옴
    # reservation_list = reservations.filter(Q(user=request.user.username, equipment_date__gf=today)|Q(user=request.user.username, equipment_date=today, equip_finish_time__gte=now))
    reservation_list = Reservation.objects.filter(Q(user=request.user.username, equipment_date__gt=today)|Q(user=request.user.username, equipment_date=today, equip_finish_time__gte=now))
    return  render(request, 'reservation/myreservation.html', {'reservation_list':reservation_list})