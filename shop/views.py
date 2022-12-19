from django.shortcuts import render, redirect
from .models import Post, Category, Company, Tag, Comment
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify
from .forms import CommentForm
from django.shortcuts import get_object_or_404
from django.db.models import Q



class PostUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'image', 'price', 'product_code', 'company', 'category']
    template_name = 'shop/post_update_form.html'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostUpdate, self).get_context_data()
        if self.object.tags.exists:
            tag_str_list = list()
            for t in self.object.tags.all():
                tag_str_list.append(t.name)
            context['tags_str_default'] = ','.join(tag_str_list)
        context['categories'] = Category.objects.all
        context['no_category_post_count'] = Post.objects.filter(category=None).count
        context['companies'] = Company.objects.all
        context['no_company_post_count'] = Post.objects.filter(company=None).count
        return context

    def form_valid(self, form):
        response = super(PostUpdate, self).form_valid(form)
        self.object.tags.clear()
        tags_str = self.request.POST.get('tags_str')
        if tags_str:
            tags_str = tags_str.strip()
            tags_str = tags_str.replace(';', ',')
            #;는 ,로 바꿔줌
            tag_list = tags_str.split(',')
            for t in tag_list:
                t = t.strip()
                tag, is_tag_created = Tag.objects.get_or_create(name=t)
                if is_tag_created:
                    tag.slug = slugify(t, allow_unicode=True)
                    tag.save()
                self.object.tags.add(tag)
        return response


class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'image', 'price', 'price', 'product_code', 'company', 'category']
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
                tags_str = tags_str.replace(';', ',')
                #;는 ,로 바꿔줌
                tag_list = tags_str.split(',')
                for t in tag_list:
                    t = t.strip()
                    tag, is_tag_created = Tag.objects.get_or_create(name=t)
                    if is_tag_created:
                        tag.slug = slugify(t, allow_unicode=True)
                        tag.save()
                    self.object.tags.add(tag)
            return response
        else:
            return redirect('/shop/')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostCreate, self).get_context_data()
        context['categories'] = Category.objects.all
        context['no_category_post_count'] = Post.objects.filter(category=None).count
        context['companies'] = Company.objects.all
        context['no_company_post_count'] = Post.objects.filter(company=None).count
        return context


class PostList(ListView):
    model = Post
    ordering = '-pk'
    paginate_by= 9
    #>>cbv 페이지

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all
        context['no_category_post_count'] = Post.objects.filter(category=None).count
        context['companies'] = Company.objects.all
        context['no_company_post_count'] = Post.objects.filter(company=None).count
        return context
    #템플릿은 모델명_list.html : post_list.html
    #매개변수 모델명_list : post_list라는 데이터 전달


class PostSearch(PostList):
    # ListView를 상속받음, post_list, post_list.html
    paginate_by = None

    def get_queryset(self):
        q = self.kwargs['q']
        post_list = Post.objects.filter(Q(title__contains=q) | Q(tags__name__contains=q)).distinct()
        return post_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostSearch, self).get_context_data()
        q = self.kwargs['q']
        context['search_info'] = f'Search: {q} ({self.get_queryset().count()})'
        return context


class PostDetail(DetailView):
    model = Post
    #cbv

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all
        context['no_category_post_count'] = Post.objects.filter(category=None).count
        context['companies'] = Company.objects.all
        context['no_company_post_count'] = Post.objects.filter(company=None).count
        context['comment_form'] = CommentForm
        return context


    #템플릿은 모델명_detail.html : post_detail.html
    #매개변수 모델명: post

def new_comment(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)
        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
        else:  # POST아닌 GET일 떄
            return redirect(post.get_absolute_url())
    else:
        raise PermissionDenied


def delete_comment(request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        if request.user.is_authenticated and request.user == comment.author:
            comment.delete()
            return redirect(comment.get_absolute_url())
        else:
            PermissionDenied

class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm

    # comment_form
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(CommentUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


def scrap(request, pk):
    post = get_object_or_404(Post, pk=pk) # pk값에 해당하는 게시물 받아옴
    user = request.user
    if user in post.scrap.all(): # 요청 유저가 이미 스크랩을 했으면
        post.scrap.remove(user) # 유저 삭제
    else: # 스크랩을 아직 안한 유저라면
        post.scrap.add(user) # 스크랩 목록에 요청 유저 추가
    return redirect('post_detail', pk)

def scrap_list(request):
    user = request.user
    return render(request, 'mypage.html', {'user':user})



def category_page(request, slug1):
    if slug1 == 'no_category':
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug1=slug1)
        post_list = Post.objects.filter(category=category)
    return render(request, 'shop/post_list.html', {
                    'category': category,
                    'post_list': post_list,
                    'categories': Category.objects.all(),
                    'no_category_post_count': Post.objects.filter(category=None).count,
                    'companies': Company.objects.all(),
                    'no_company_post_count': Post.objects.filter(company=None).count
    })


def company_page(request, slug):
    if slug == 'no_company':
        company = '미분류'
        post_list = Post.objects.filter(company=None)
    else:
        company = Company.objects.get(slug=slug)
        post_list = Post.objects.filter(company=company)
    return render(request, 'shop/post_list.html', {
                    'company': company,
                    'post_list': post_list,
                    'companies': Company.objects.all(),
                    'no_company_post_count': Post.objects.filter(company=None).count,
                    'categories': Category.objects.all(),
                    'no_category_post_count': Post.objects.filter(category=None).count
    })


def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all()
    return render(request, 'shop/post_list.html', {
        'tag': tag,
        'post_list': post_list,
        'categories': Category.objects.all(),
        'no_category_post_count': Post.objects.filter(category=None).count,
        'companies': Company.objects.all(),
        'no_company_post_count': Post.objects.filter(company=None).count
    })


#query로 post목록 가져오기
#def index(request):
    #posts=Post.objects.all().order_by('pk')
    #return render(request, 'blog\index.html', {'posts':posts})

#def single_post_page(request,pk):
    #post = Post.objects.get(pk=pk)
    #return render(request,'blog/single_post_page.html',{'post':post})