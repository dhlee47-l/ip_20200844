from django.shortcuts import render #redirect
from shop.models import Post #Comment


# Create your views here.
def landing(request):
    recent_post = Post.objects.order_by('-pk')[:3]
    return render(request, 'single_pages/landing.html',{
        'recent_posts' : recent_post,
    })

def about_me(request):
    return render(request,'single_pages/about_me.html')

def mypage(request):
    return render(request, 'single_pages/mypage.html')

# def comments(response, comments):
#     comments = Comment.comments.objects.all(pk=comments)
#     return render(response,'single_pages/mypage.html',{'comments':comments})




