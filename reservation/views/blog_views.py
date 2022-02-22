from django.shortcuts import render, get_object_or_404
from ..models import Blog

def detail(request, blog_id):
    blog_detail = get_object_or_404(Blog, pk=blog_id) # 특정 객체 가져오기
    return render(request, 'reservation/detail.html', {'blog':blog_detail})

def index(request, category_name):
    blogs = Blog.objects.filter(category=category_name).order_by('-created')
    category = category_name
    return render(request, 'reservation/index.html', {'category':category, 'blogs':blogs})
