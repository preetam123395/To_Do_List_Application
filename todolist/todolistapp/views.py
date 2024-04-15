from django.shortcuts import render,HttpResponseRedirect,get_object_or_404,redirect
from .forms import SignUpForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from .models import Task
from .forms import TaskForm
from django.contrib.auth.decorators import login_required

# signup view function.
def sign_up(request):
 if request.method == "POST":
  fm = SignUpForm(request.POST)
  if fm.is_valid():
   fm.save()
   messages.add_message(request,messages.SUCCESS,'your account created !!!')
#    messages.success(request,'your account created !!!')
   fm = SignUpForm()
   return render(request,'enroll/signup.html',{'form':fm})
 else: 
  fm = SignUpForm()
 return render(request, 'enroll/signup.html', {'form':fm})


#login view function
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            fm = AuthenticationForm(request, data=request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Logged in successfully !!')
                    return HttpResponseRedirect('/profile/')
                else:
                    messages.error(request, 'Invalid username or password')  # Display error for incorrect credentials
            else:
                messages.error(request, 'Invalid username or password')  # Display error for form validation issues
        else:
            fm = AuthenticationForm()
        return render(request, 'enroll/userlogin.html', {'form': fm})
    else:
        return HttpResponseRedirect('/profile/')
    

def user_logout(request):
  logout(request)
  return HttpResponseRedirect('/login/')

 
def user_profile(request):
    if request.user.is_authenticated:
        data =Task.objects.filter(user=request.user)
        return render(request,'enroll/profile.html',{'tasks':data})
    else:
         return HttpResponseRedirect('/login/')
       
@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
           data = form.cleaned_data
           create_task = Task.objects.create(user=request.user,title=data['title'],description=data['description'],completed=data['completed'])
           deta =Task.objects.filter(user=request.user)
           return render(request,'enroll/profile.html',{'tasks':deta})
    form = TaskForm()
    return render(request, 'enroll/create_task.html', {'form': form})    
       
@login_required
def edit_task(request,id):
    task = Task.objects.get(id=id)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task.title = form.cleaned_data['title']
            task.description = form.cleaned_data['description']
            task.completed = form.cleaned_data['completed']
            task.save()
            return HttpResponseRedirect('/profile/')
    else:
        initial_data = {
            'title': task.title,
            'description': task.description,
            'completed': task.completed,
        }
        form = TaskForm(initial=initial_data)
    return render(request, 'enroll/edit_task.html', {'form': form})


@login_required
def delete_task(request, id):
    task = get_object_or_404(Task,id=id)
    task.delete()
    return HttpResponseRedirect('/profile/')   

def change_password(request):
   if request.user.is_authenticated:
      
    if request.method=="POST":
        form = PasswordChangeForm(user=request.user,data=request.POST)
        if form.is_valid():
            form.save()
        update_session_auth_hash(request,form.user)
        return HttpResponseRedirect('/profile/')

    else:
      form = PasswordChangeForm(user=request.user)
      return render(request, 'enroll/change_pass.html', {'form': form})
      
   else:
       return HttpResponseRedirect('/login/')



   

           
        

        
            
    

