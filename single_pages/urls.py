from django.urls import path
from. import views

urlpatterns=[#IP주소/blog/
    path('', views.landing),
    path('about_me/', views.about_me),
    path('mypage/', views.mypage)
    #path('', views.index), #IP주소/blog/
    #path('<int:pk:/', views.single_post_page)
    #blog/views변경
]