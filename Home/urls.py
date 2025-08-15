from django.contrib import admin
from django.urls import path
from Home import views
# student_project/urls.py
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.index, name="index"),
    path("signup", views.signup, name="signup"),
    path("adminpage", views.adminpage, name="adminpage"),
    path("login", views.login, name="login"),
    path("createEvent", views.createEvent, name="createEvent"),
    path("logout", views.logout, name="logout"),
    path("student_register", views.student_register, name="student_register"),
    path('upload_excel', views.upload_excel, name='upload_excel'),
]