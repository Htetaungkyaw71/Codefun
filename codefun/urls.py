from django.urls import path
from . import views

urlpatterns = [
    path('create',views.index,name="home"),
    path('',views.main,name="main"),
    path('login',views.login_view,name="login"),
    path('register',views.register_view,name="register"),
    path('logout',views.logout_view,name="logout"),
    path('otp',views.otp_view,name="otp"),
    path('detail/<int:id>',views.detail,name="detail"),
    path('edit/<int:id>',views.edit,name="edit"),
    path('editpp/<int:id>',views.editpp,name="editpp"),
    path('deletepp',views.deletepp,name="deletepp"),
    path('delete/<int:id>',views.delete,name="delete"),
    path('profile/<int:id>',views.profile,name="profile"),
    path('search',views.search,name="search"),
]
