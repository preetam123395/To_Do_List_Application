from django.contrib import admin
from django.urls import path
from todolistapp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', views.sign_up,name='signup'),
    path('login/',views.user_login,name='login'),
    path('profile/',views.user_profile,name='profile'),
    path('logout/',views.user_logout,name='logout'),
    path('change_password/',views.change_password,name='change_password'),
    path('create/', views.create_task, name='create_task'),
    path('edit/<int:id>/', views.edit_task, name='delete_task'),
    path('delete/<int:id>/', views.delete_task, name='delete_task')

]