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

def detail(request, blog_id):
    blog_detail = get_object_or_404(Blog, pk=blog_id) # 특정 객체 가져오기
    return render(request, 'reservation/detail.html', {'blog':blog_detail})

def index(request, category_name):
    blogs = Blog.objects.filter(category=category_name).order_by('-created')
    category = category_name
    return render(request, 'reservation/index.html', {'category':category, 'blogs':blogs})

def edit(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    min_date = datetime.now().strftime("%Y-%m-%d") # 오늘부터
    max_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d") # 14일 후까지 가능
    return render(request, 'reservation/edit.html', {'reservation':reservation, 'min_date':min_date, 'max_date':max_date})

def update(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    reservation.equipment_type = request.GET['equipment_type']
    reservation.equip_date = request.GET['equipment_date']
    reservation.equip_start_time = request.GET['equip_start_time']
    reservation.equip_finish_time = request.GET['equip_finish_time']
    reservation.save()

    return redirect('/reservation/'+str(reservation.id)) # 새로운 예약 url 주소로 이동

def delete(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    if reservation.user == request.user.username:
        reservation.delete()
    return redirect('/reservation/my')

def myreservation(request):
    today = date.today() # 오늘 날짜
    now_time = datetime.now() # ex) (2007, 12, 6, 16, 29, 43, 79043)
    now = now_time.hour + (now_time.minute/60) # 현재 시간 # 왜 60으로나누는거지?
    reservations = Reservation.objects.all()
    # 장비 예약 날짜가 오늘보다 크거나 끝나는시간이 지금보다 나중일때 목록을 불러옴
    reservation_list = reservations.filter(Q(user=request.user.username, equipment_date__gf=today)|Q(user=request.user.username, equipment_date=today, equip_finish_time=now))
    return  render(request, 'reservation/myreservation.html', {'reservation_list':reservation_list})
# ajax
def check(request):
    equipment_type_vr = request.POST.get('equipment_type', None)
    equipment_date_vr = request.POST.get('equipment_date', None)  # ajax 통신으로 template에서 POST방식으로 전달
    equip_start_time_vr = request.POST.get('equip_start_time', None)
    equip_finish_time_vr = request.POST.get('equip_finish_time', None)

    reservations = Reservation.objects.all()
    # reserve_date = datetime.strptime(equipment_date_vr, "%Y-%m-%d ").date()
    check_error = 0 # 정상

    # 겹치는 시간 있는지 체크
    message = "이미 예약된 시간입니다."

    # 고쳐봐야겠음 왜 if로 하지 ?
    # <1> 오른쪽 겹치기
    # start 시간보다 크고 finish 시간보다 작다
    if reservations.filter(equipment_type = equipment_type_vr, equipment_date=equipment_date_vr, equip_finish_time__gt=equip_start_time_vr, equip_start_time__lt=equip_finish_time_vr).count() != 0:
        check_error = 1
        context = {
            "message":message,
            'check_error':check_error
        }
        return HttpResponse(json.dumps(context), content_type="application/json")
    # <2> 사이 들어가기
    # start 시간보다 작거나 같고 finish 시간보다 크거나 같다
    if reservations.filter(equipment_type = equipment_type_vr, equipment_date=equipment_date_vr, equip_finish_time__lte=equip_start_time_vr, equip_start_time__gte=equip_finish_time_vr).count() != 0:
        check_error = 1
        context = {
            "message":message,
            'check_error':check_error
        }
        return HttpResponse(json.dumps(context), content_type="application/json")
    # <3> 오른쪽 포개지기
    # start 시간보다 작고 finish 시간보다 크다
    if reservations.filter(equipment_type = equipment_type_vr, equipment_date=equipment_date_vr, equip_finish_time__lt=equip_finish_time_vr, equip_start_time__gt=equip_start_time_vr).count() != 0:
        check_error = 1
        context = {
            "message":message,
            'check_error':check_error
        }
        return HttpResponse(json.dumps(context), content_type="application/json")
    # <4> 밖에 감싸기
    # start 시간보다 크거나 같고 finish 시간보다 작거나 같다
    if reservations.filter(equipment_type = equipment_type_vr, equipment_date=equipment_date_vr, equip_finish_time__gte=equip_start_time_vr, equip_start_time__lte=equip_finish_time_vr).count() != 0:
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



