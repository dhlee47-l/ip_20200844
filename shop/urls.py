from django.urls import path
from. import views

urlpatterns=[#IP주소/blog/
    path('post_list/',views.PostList.as_view()),
    path('<int:pk>/new_comment/', views.new_comment),
    path('update_comment/<int:pk>/', views.CommentUpdate.as_view()),
    path('delete_comment/<int:pk>/', views.delete_comment),
    path('<int:pk>/', views.PostDetail.as_view(), name="post_detail"),
    path('update_post/<int:pk>/', views.PostUpdate.as_view()),
    path('create_post/', views.PostCreate.as_view()),
    path('category/<str:slug1>/', views.category_page),
    path('company/<str:slug>/', views.company_page),#IP주소/blog/category/slug
    path('tag/<str:slug>/', views.tag_page),
    path('search/<str:q>/', views.PostSearch.as_view()),
    path('scrap/<int:pk>/', views.scrap, name="scrap")

    #path('', views.index), #IP주소/blog/
    #path('<int:pk:/', views.single_post_page)
    #blog/views변경
]