from django.urls import path, include
from . import views

urlpatterns = [
     path('', views.home_page, name='home_page'),
     path('get_room/', views.get_room, name='room_page'),
     path('gym_reg/', views.gym_page, name='gym_page'),
     path('register/', views.user_reg, name='reg_page'),
     path('login/', views.login_page, name='login_page'),
     path('logout/', views.logout_page, name='logout_page'),

     path('control/', views.control_page, name='control_page'),
     path('control/checkout/<str:room_num>/', views.checkout, name='checkout'),
     path('control/checkin/<str:name>/', views.checkin, name='checkin'),

     path('getuser/<str:name>/', views.user_page2, name='user_page2'),
     path('user/', views.user_page, name='user_page'),
     
     # path('get_hall/', views.get_hall, name='hall_page'),
     # path('get_hall/book_sm_hall/', views.book_sm_hall, name='book_sm_hall'),
     # path('get_hall/book_md_hall/', views.book_md_hall, name='book_md_hall'),
     # path('get_hall/book_lg_hall/', views.book_lg_hall, name='book_lg_hall'),
]