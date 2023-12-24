from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_list", views.create_list, name="create_list"),
    path("DisplayCategory", views.DisplayCategory, name="DisplayCategory"),
    path("DisplayCategory/<str:CategoryType>/", views.DisplayItems, name="DisplayItems"),
    path('ItemDetails/<int:id>/<str:title>/', views.ItemDetails, name="ItemDetails"),
    path('watchList/', views.watchList, name="watchList"),
    path('WatchList/add_WatchList/<int:id>/', views.add_WatchList, name="add_WatchList"),
    path('WatchList/Remove_WatchList/<int:id>/', views.Remove_WatchList, name="Remove_WatchList"),
    path('AddBid/<int:id>/', views.AddBid, name="AddBid"),
    path('status/<int:id>/', views.status, name="status"),
]
