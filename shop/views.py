from django.shortcuts import render, redirect
from .models import Post, Category, Tag
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields=['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']
    template_name = 'shop/post_update_form.html'
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate,self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostUpdate, self).get_context_data()
        if self.object.tags.exists:
            tag_str_list = list()
            for t in self.object.tags.all():
                tag_str_list.append(t.name)
            context['tags_str_default'] = ','.join(tag_str_list)
        context['categories'] = Category.objects.all
        context['no_category_post_count'] = Post.objects.filter(category=None).count
        return context

    def form_valid(self, form):
            response = super(PostUpdate, self).form_valid(form)
            self.object.tags.clear()
            tags_str = self.request.POST.get('tags_str')
            if tags_str:
                tags_str = tags_str.strip()
                tags_str = tags_str.replace(';',',')
                #;는 ,로 바꿔줌
                tag_list = tags_str.split(',')
                for t in tag_list:
                    t = t.strip()
                    tag, is_tag_created = Tag.objects.get_or_create(name=t)
                    if is_tag_created:
                        tag.slug=slugify(t, allow_unicode=True)
                        tag.save()
                    self.object.tags.add(tag)
            return response



class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model=Post
    fields =['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']
    #tags 넣으면 사용자가 적는 tags가 아닌 선택하는 tags가 나타남
    #모델명_form.html이라는 템플릿 자동 호출

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_superuser or current_user.is_staff):
            form.instance.author = current_user
            response = super(PostCreate, self).form_valid(form)
            tags_str = self.request.POST.get('tags_str')
            if tags_str:
                tags_str = tags_str.strip()
                tags_str = tags_str.replace(';',',')
                #;는 ,로 바꿔줌
                tag_list = tags_str.split(',')
                for t in tag_list:
                    t = t.strip()
                    tag, is_tag_created = Tag.objects.get_or_create(name=t)
                    if is_tag_created:
                        tag.slug=slugify(t, allow_unicode=True)
                        tag.save()
                    self.object.tags.add(tag)
            return response
        else:
            return redirect('/shop/')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostCreate, self).get_context_data()
        context['categories'] = Category.objects.all
        context['no_category_post_count'] = Post.objects.filter(category=None).count
        return context

# Create your views here.
class PostList(ListView):
    model=Post
    ordering ='-pk'
    #>>cbv 페이지

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all
        context['no_category_post_count'] = Post.objects.filter(category=None).count
        return context
    #템플릿은 모델명_list.html : post_list.html
    #매개변수 모델명_list : post_list라는 데이터 전달

class PostDetail(DetailView):
    model = Post
    #cbv

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all
        context['no_category_post_count'] = Post.objects.filter(category=None).count
        return context

    #템플릿은 모델명_detail.html : post_detail.html
    #매개변수 모델명: post


def category_page(request, slug):
    if slug == 'no_category':
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else :
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)
    return render(request, 'shop/post_list.html'
                  #fbv스타일
                  , {
        'category' : category,
        'post_list': post_list,
        'categories' : Category.objects.all(),
        'no_category_post_count': Post.objects.filter(category=None).count
    })

def tag_page(request, slug):
    tag=Tag.objects.get(slug=slug)
    post_list = tag.post_set.all()
    return render(request, 'category/post_list.html', {
        'tag' : tag,
        'post_list' : post_list,
        'categories': Category.objects.all(),
        'no_category_post_count': Post.objects.filter(category=None).count
    })


#query로 post목록 가져오기
#def index(request):
    #posts=Post.objects.all().order_by('pk')
    #return render(request, 'blog\index.html', {'posts':posts})

#def single_post_page(request,pk):
    #post = Post.objects.get(pk=pk)
    #return render(request,'blog/single_post_page.html',{'post':post})