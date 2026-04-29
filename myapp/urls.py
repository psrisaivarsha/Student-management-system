from django.urls import path
from myapp import views

urlpatterns = [
    path('', views.home, name='home'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('students/', views.getStudents, name='students'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('signup/', views.signup_view, name='signup'),
    path('register/', views.registerStudent, name='register'),
    path('find/<int:id>/', views.getStudent, name='find'),
    path('edit/<int:id>/', views.editStudent, name='edit'),
    path('delete/<int:id>/', views.deleteStudent, name='delete'),
    path('image/<int:id>/', views.upload_image, name='image'),
]