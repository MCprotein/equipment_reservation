from django.shortcuts import render, get_object_or_404, redirect
from .models import Reservation, Blog
from django.utils import timezone
from datetime import datetime, timedelta, date
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import json, time
from django.db.models import Q

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
        start_day = today # 시작 지금
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

    #  월~금