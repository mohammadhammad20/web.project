from django.urls import path
from . import views
urlpatterns=[
    path('signup/',views.signup),
    path('signin/',views.signin),
    path('logout',views.logout),
    path('home/',views.home),
    path('my-courses/',views.my_courses),
    path('course-details/<int:pk>',views.coures_details),
    path('course-select/<int:pk>',views.course_select),
]