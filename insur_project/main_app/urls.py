from django.urls import path
from . import views

urlpatterns = [
    path('view-all/', views.ViewAll.as_view()),
    path('user-detail/<str:pk>/', views.UserDetail.as_view()),
    path('active-contracts/', views.ActiveContracts.as_view()),
    path('chart/day/<str:pk>/', views.ChartDay.as_view()),
    path('vehicle-detail/<str:pk>/', views.VehicleDetail.as_view()),
    path('create-user/', views.CreateUser.as_view())
]
