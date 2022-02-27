from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from ..models import Blog
from ..forms import BlogCreateForm
from django.contrib import messages
from django.utils import timezone

def blog_detail(request, blog_id):
    blogs = get_object_or_404(Blog, pk=blog_id) # 특정 객체 가져오기
    return render(request, 'reservation/blog_detail.html', {'blogs':blogs})

def blog_index(request, category_name):
    blogs = Blog.objects.filter(category=category_name).order_by('-created')
    category_name = category_name
    return render(request, 'reservation/blog_index.html', {'category_name':category_name, 'blogs':blogs})

@login_required(login_url='accounts:login')
def blog_create(request, category_name):
    """
    blog 글 등록
    """
    if request.method == 'POST':
        form = BlogCreateForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user # author 속성에 로그인 계정 저장
            blog.category = request.POST['category']
            blog.save()
            return redirect('reservation:blog_index', category_name=blog.category)
    else:
        form = BlogCreateForm()
    context = {'form': form}
    return render(request, 'reservation/blog_form.html', context)

@login_required(login_url='accounts:login')
def blog_modify(request, blog_id):
    """
    blog 글 수정
    """
    blog = get_object_or_404(Blog, pk=blog_id)
    if request.user != blog.author:

        messages.error(request, '수정 권한이 없습니다.') # messages: 장고가 제공하는 모듈, 넌필드오류를 발생시킬때 사용
        return redirect('reservation:blog_detail', blog_id=blog_id)

    if request.method == "POST":
        form = BlogCreateForm(request.POST, instance=blog)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.updated = timezone.now() # 수정일시 저장,
            blog.save()
            return redirect('reservation:blog_detail', blog_id=blog_id)
    else:
        form = BlogCreateForm(instance=blog) # GET요청일 경우 글 수정 화면에 조회된 글의 제목과 내용이 반영
    context = {'form':form}
    return render(request, 'reservation/blog_form.html', context)

@login_required(login_url='accounts:login')
def blog_delete(request, blog_id, category_name):
    """
    blog 글 삭제
    """
    blog = get_object_or_404(Blog, pk=blog_id)
    if request.user != blog.author:
        messages.error(request, '삭제 권한이 없습니다.')
        return redirect('reservation:blog_detail', blog_id=blog_id)
    blog.delete()
    return redirect('reservation:blog_index', category_name=category_name)