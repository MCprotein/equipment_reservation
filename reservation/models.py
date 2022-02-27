from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
class Reservation(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_reservation')
    # user = models.CharField(max_length=10)
    equipment_type = models.CharField(max_length=10) # 장비 종류
    equipment_date = models.DateField(max_length=20) # 장비 날짜
    equip_start_time = models.FloatField() # 시작 시간 0900
    equip_finish_time = models.FloatField() # 종료 시간 2100
    created = models.DateTimeField(auto_now_add=True) # 언제 예약 신청을 했는지

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.Author

class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='user_blog')
    category = models.CharField(max_length=20, default='공지사항') # 게시판 카테고리, 기본값:공지사항
    title = models.CharField(max_length=200) # 제목
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)
    description = RichTextUploadingField(blank=True, null=True) # ckeditor # 내용

    class Meta:
        ordering = ['-created', '-updated']

    def __str__(self):
        return self.title