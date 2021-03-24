from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

from . import views
from django.urls import path, include
app_name="dashboard"

urlpatterns = [
    path('', views.login_, name='login'),
    path('logout', views.logout_, name='logout'),
    path('register', views.register_, name='register'),
    path('dashboard',views.dashboard,name='index'),
    path('profile/',views.profile_,name='profile'),
    path('edit/',views.edit,name='edit'),   
    path('task_list/', views.TaskListView.as_view(), name='task_list'),
    path('task_list/create/', views.TaskCreateView.as_view(), name='task_create'),
    path('task_list/<int:pk>/', views.TaskDetailView.as_view(), name='task_detail'),
    path('task_list/<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),
    path('task_list/<int:pk>/take/', views.take_task, name='task_take'),
    path('task_list/<int:pk>/done/', views.task_done, name='task_done'),

]