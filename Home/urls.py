from django.contrib import admin
from django.urls import path
from Home import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.index, name="index"),
    path("signup", views.signup, name="signup"),
    path("adminpage", views.adminpage, name="adminpage"),
    path("login", views.login, name="login"),
    path("createEvent", views.createEvent, name="createEvent"),
    path("logout", views.logout, name="logout"),
    path("student_register", views.student_register, name="student_register"),
    path('editEvent/<int:event_id>/', views.editEvent, name='editEvent'),
]