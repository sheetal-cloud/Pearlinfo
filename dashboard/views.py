from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string, get_template
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from .models import profile,Task
from django.contrib.auth.models import User, auth
from django.core.mail import send_mail
from django.core.mail import EmailMessage,BadHeaderError,EmailMultiAlternatives
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from django.utils import timezone
import datetime

# from twilio.rest import Client
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)

def login_(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        username = get_user(email)
        print(username)
        user = authenticate(username=username, password=password)
        if user:
            login(request,user)
            return redirect('dashboard:index')
        else:
            print("Someone tried to login and failed.")
            print("They used email: {} and password: {}".format(email,password))
            return HttpResponse("Invalid login details given")
         
    else:
        return render(request, 'login.html', {})
   
    
def register_(request):
    alert = {
        
    }
    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        if User.objects.filter(username = request.POST['username']).exists():
            alert['message'] = "Username already exists"
        elif User.objects.filter(email = request.POST['email']).exists():
            alert['message'] = "email already exists"
        else:
            username=request.POST.get('username')
            email=request.POST.get('email')
            password=request.POST.get('password')
            usr=User.objects.create_user(username=username,email=email,password=password)
            try:
                message = "Thank you for registering to our site"
                subject = 'Thank you for registering to our site'
                email_from = settings.EMAIL_HOST_USER
                to_email = usr.email
                send_mail(
                        subject,
                        message,
                        email_from,
                        [to_email],
                        fail_silently=False
                    )
                return redirect('/')
                print('success')
            except BadHeaderError:
                print('erroe')
                ins=User.objects.get(email__exact=request.POST.get('email')).delete()
                print(ins)
                alert['message']="email not send"
            
    return render(request, 'register.html',alert)


def dashboard(request):
    return render(request, 'dashboard.html')


def get_user(email):
    try:
        return User.objects.get(email=email.lower())
    except User.DoesNotExist:
        return None 

 
def logout_(request):
    logout(request)
    return redirect('dashboard:login')

@login_required(login_url="/") 
def profile_(request):
    u=profile.objects.get(user_id=request.user)
    use=User.objects.get(username=request.user)
    context={}
    context['profile']=u
    if request.method=='POST':
       email=request.POST.get('email')
       first_name=request.POST.get('first_name')
       last_name=request.POST.get('last_name')
       username=request.POST.get('username')
       address=request.POST.get('address')
       genre=request.POST.get('genre')
       birth_date=request.POST.get('birth_date')
       if birth_date==None:
           birth_date=u.birth_date
       locatity=request.POST.get('locatity')
       use.first_name=first_name
       use.last_name=last_name
       use.username=username
       use.email=email
       u.address=address
       u.locatity=locatity
       u.birth_date=birth_date
       u.genre=genre
       use.save()
       u.save()
       return redirect('dashboard:profile')  
    return render(request,'user.html',context)

@login_required(login_url="/") 
def edit(request):
    u=profile.objects.get(user_id=request.user)
    use=User.objects.get(username=request.user)
    context={}
    context['profile']=u
    if request.method=='POST' and request.FILES:
        bgprofile=request.FILES.get('bgprofile')
        profile1=request.FILES.get('profile1')
        if bgprofile==None:
            bgprofile=u.bgprofile  
        if profile1==None:
            profile1=u.profile1
        u.bgprofile=bgprofile
        u.profile1=profile1
        u.save()
        return redirect('dashboard:edit')

    return render(request,'edit.html',context)  


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = '/task_list/'

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['task_name','task_desc']
    success_url = '/task_list/'
    extra_context = {
        'title': 'Create Task'
    }

    def get_context_data(self, *args, **kwargs):
        kwargs.update(self.extra_context)
        return super().get_context_data(*args, **kwargs)

    def form_valid(self, form):
        form.instance.task_creator = self.request.user
        form.instance.task_created = timezone.now
        return super().form_valid(form)

def take_task(request, pk):
    task = Task.objects.get(pk=pk)
    task.task_taker = request.user.username
    task.time_taken = timezone.now()
    task.save()
    return redirect('dashboard:task_list')

def task_done(request, pk):
    task = Task.objects.get(pk=pk)
    task.time_done = timezone.now()
    task.save()
    return redirect('dashboard:task_list')

