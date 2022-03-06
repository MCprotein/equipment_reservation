from django.contrib.auth.models import User
from django import forms

# 폼은 뷰에서 쓴다
# 폼 : 폼태그 -> HTML의 태그 -> 프론트단에서 사용자의 입력을 받는 인터페이스
# 장고의 폼 : HTML의 폼 역할, 데이터베이스에 저장할 내용의 형식, 제약조건 결정
class RegisterForm(forms.ModelForm):
    password = forms.CharField(label='비밀번호', widget=forms.PasswordInput)
    password2 = forms.CharField(label='비밀번호 확인', widget=forms.PasswordInput)
    department = forms.CharField(label='부서')


    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            'username': '아이디',
            'first_name': '이름',
            'last_name': '성',
            'email': '이메일',
            'password': '비밀번호',
            'password2': '비밀번호 확인',
            'department': '부서',
        }
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('비밀번호 확인이 일치하지 않습니다.')
        return cd['password2']