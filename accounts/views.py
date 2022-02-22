from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Profile
from datetime import datetime
from reservation.models import Reservation, Blog
from django.contrib import auth

# 비밀번호 찾기 관련
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse_lazy

# SMTP 관련 인증
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token

def signup(request):

    if request.method == "POST":
        if request.POST['password1'] == request.POST['password2']: # 추후 forms.py로 변경
            # 유저 만들기
            mail_to = request.POST['email'] + "@gmail.com" # 지메일 # 추후 구글웹로그인으로 변경

            # 이메일 중복일 경우 실패
            if len(User.objects.filter(email=mail_to)) == 0:
                new_user = User.objects.create_user(username=request.POST['username'], email=mail_to, password=request.POST['password1'])
                new_user.is_active = False
                new_user.save()
                realname = request.POST['realname'] # 이름
                department = request.POST['department'] # 소속
                profile = Profile(user=new_user, realname=realname, department=department)
                profile.save() # 프로필 저장

                current_site = get_current_site(request)
                message = render_to_string('accounts/activation_email.html', {
                    'user': new_user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                    'token': account_activation_token.make_token(new_user),
                })
                mail_title = "티엠디랩 실험실 장비 예약 시스템 계정 활성화 확인"
                email = EmailMessage(mail_title, message, to=[mail_to])
                email.send()
                today = datetime.now()
                equip_Hood = Reservation.objects.filter(equipment_date=today, equipment_type='Hood')
                equip_Chiller = Reservation.objects.filter(equipment_date=today, equipment_type='Chiller')
                equip_Press = Reservation.objects.filter(equipment_date=today, equipment_type='Press')
                equip_Dsc = Reservation.objects.filter(equipment_date=today, equipment_type='Dsc')
                equip_Gpc = Reservation.objects.filter(equipment_date=today, equipment_type='Gpc')
                equip_Utm = Reservation.objects.filter(equipment_date=today, equipment_type='Utm')
                equip_Crosslinker = Reservation.objects.filter(equipment_date=today, equipment_type='Crosslinker')
                proportion = [0,0,0,0,0,0,0]
                for r in equip_Hood:
                    proportion[0] += (r.equip_finish_time - r.equip_start_time)
                for r in equip_Chiller:
                    proportion[1] += (r.eqiup_finish_time - r.equip_start_time)
                for r in equip_Press:
                    proportion[2] += (r.eqiup_finish_time - r.equip_start_time)
                for r in equip_Dsc:
                    proportion[3] += (r.eqiup_finish_time - r.equip_start_time)
                for r in equip_Gpc:
                    proportion[4] += (r.eqiup_finish_time - r.equip_start_time)
                for r in equip_Utm:
                    proportion[5] += (r.eqiup_finish_time - r.equip_start_time)
                for r in equip_Crosslinker:
                    proportion[6] += (r.eqiup_finish_time - r.equip_start_time)

                notice_list = Blog.objects.filter(category="공지사항").order_by('created') # 공지사항
                notices = notice_list[0:3] # 최근 3개 글만 보여줌
                lost_list = Blog.objects.filter(category="분실물").order_by('created') #분실물
                losts = lost_list[0:3] # 최근 3개 글만 보여줌
                msg = mail_to+ "주소로 인증 메일을 발송하였습니다. 입력하신 메일을 확인하여 인증을 완료해주세요."
                return render(request, 'reservation/home.html', {'msg':msg, 'notices':notices, 'losts':losts, 'proportion':proportion})
            else:
                msg = mail_to + "의 이메일로 인증한 계정이 존재합니다. 비밀번호 재설정을 이용해주세요"
                return render(request, 'accounts/login.html', {'msg':msg})
    # 포스트 방식 아니면 페이지 띄우기
    return render(request, 'accounts/signup.html')

# 메일 확인
def confirm(request):
    return render(request, 'accounts/confirm.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'accounts/login.html', {'msg':'입력 정보가 올바르지 않습니다.'})
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')
    return render(request, 'accounts/signup.html')

def activate(request, uid64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uid64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth.login(request, user)
        return redirect("home")
    else:
        notice_list = Blog.objects.filter(category="공지사항").order_by('-created')
        notices = notice_list[0:3]

        lost_list = Blog.objects.filter(category="분실물").order_by('-created')
        losts = lost_list[0:3]
        return render(request, 'reservation/home.html', {'notices':notices, 'losts':losts, 'msg': '이메일 인증 오류가 발생하였습니다.'})

class MyPasswordResetView(PasswordResetView):
    success_url = reverse_lazy('login')
    template_name = 'accounts/password_reset_form.html'
    email_template_name = 'accounts/password_reset.html'
    mail_title="비밀번호 재설정"

    def form_valid(self, form):
        return super().form_valid(form)

class MyPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy('login')
    template_name = 'accounts/password_reset_confirm.html'

    def form_valid(self, form):
        return super().form_valid(form)