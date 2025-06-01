from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('calculate/',views.calc,name="calculate"),
    path('proceed/', views.proceed, name='proceed'),
    path('point/', views.point, name='point'),
]