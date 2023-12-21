from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import Group
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .models import User
from .forms import CreateUserForm
from dtks.models import Kecamatan, Bansos
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users
# from django.contrib.auth.models import User

# Create your views here.
@unauthenticated_user
def loginView(request):
  context={
        'title':'Login',
    }
  user=None
  if request.method=='POST':
      username = request.POST.get('username')
      password = request.POST.get('password')
      
      user = authenticate(request, username=username, password=password)

      if user is not None :
        if user.groups.all()[0].name == "Superadmin" or user.groups.all()[0].name == "Admin":
          login(request, user)
          messages.success(request, 'Login Success! Welcome '+user.name)
          return redirect ('dashboard')
        elif user.groups.all()[0].name == "TKSK":
          login(request, user)
          messages.success(request, 'Login Success! Welcome '+user.name)
          return redirect ('tksk:dashboard')
      else:
        messages.error(request, 'Login Failed! Please enter username and password correctly')  
        return redirect ('account:login')
  # if request.method=="GET":
  #     if request.user.is_authenticated():
  #       return redirect ('data_bansos:sembako_lansia')
  #     else:
  return render(request, 'account/login.html', context)

@login_required(login_url='account:login')
def logoutView(request):
  
  logout(request)
  messages.success(request, 'Logout Success!')  
  return redirect('account:login')

@login_required(login_url='account:login')
@allowed_users(allowed_roles=['Superadmin'])
def registration(request):
  form = CreateUserForm()
  if request.method =='POST':
    role = request.POST.get('role')
    form = CreateUserForm(request.POST)
    if form.is_valid():
      user = form.save()
      username = form.cleaned_data.get('username')
      group = Group.objects.get(name=role)
      user.groups.add(group)
      messages.success(request, 'Account was created for ' + username)
      if request.POST.get("add"):
        return HttpResponseRedirect(reverse('account:user'))
      elif request.POST.get("add_another"):  # You can use else in here too if there is only 2 submit types.
        return HttpResponseRedirect(reverse('account:registration'))
  context={
    'title':'Create User',
    'form':form
  }
  return render(request, 'account/registration.html', context)

@login_required(login_url='account:login')
@allowed_users(allowed_roles=['Superadmin'])
def user(request):
  user = User.objects.exclude(groups__name='Superadmin')
  kecamatan = Kecamatan.objects.all()
  bansos = Bansos.objects.all()
  form = CreateUserForm()

  
  # if User.objects.filter(role='Pimpinan'):
  #   badge="primary"
  # elif role == 'Pimpinan':
  #   badge="success"
  # else :
  #   badge = "warning"
  context = {
    'title' : 'User',
    'data_user'  : user,
    'badge' : 'success',
    'no'    : 1,
    'form'  : form,
    'kecamatan' : kecamatan,
    'bansos' : bansos,
  }
  # if request.method == 'POST':
  #   nama = request.POST['nama']
  #   username = request.POST['username']
  #   password = request.POST['password']
  #   location = request.POST['location']
  #   # new_user = User(name=nama,username=username,password=password,role=role,location=location)
  #   new_user=User.objects.create_user(name=nama,username=username,location=location)
  #   new_user.set_password(password)
  #   new_user.save()
  #   return redirect ('account:user')
  
  return render(request, 'account/user.html', context)

def delete(request, id):
  User.objects.filter(id=id).delete()
  return redirect ('account:user')

def update(request, id):
  
  if request.method == 'POST':
    # newpassword = request.POST['newpassword']
    role = request.POST.get('newrole')
    newnama = request.POST.get('newnama')
    newusername = request.POST.get('newusername')
    newlocation = request.POST.get('newlocation')
    group = Group.objects.get(name=role)
    user = User.objects.get(id=id)
    user.groups.clear()
    user.groups.add(group)
    user.name = newnama
    user.username = newusername
    user.location = newlocation
    # user.set_password(newpassword)
    user.save()
    messages.success(request, 'User updated!')
    return redirect ('account:user')

@login_required(login_url='account:login')
def profile(request, id):
  data_user = User.objects.get(id=id)
  bansos = Bansos.objects.all()

  if request.method == 'POST':
    form = PasswordChangeForm(request.user, request.POST)
    if form.is_valid():
      user = form.save()
      update_session_auth_hash(request, user)  # Important!
      messages.success(request, 'Your password was successfully updated!')
      return redirect('account:profile')
    else:
      messages.error(request, 'Please correct the error below.')
  else:
      form = PasswordChangeForm(request.user)
      
  if request.user.groups.all()[0].name == "TKSK":
    base = 'base_tksk.html'
  else:
    base = 'base.html'
  context={
    'title':'User Profile',
    'user': data_user,
    'base':base,
    'bansos':bansos,
    'form': form
  }
  return render(request, 'account/profile.html', context)

def update_profile(request, id):
  if request.method == 'POST':
    newnama = request.POST.get('nama')
    newusername = request.POST.get('username')
    user = User.objects.get(id=id)
    user.name = newnama
    user.username = newusername
    user.save()
    messages.success(request, 'Profil updated!')
    return HttpResponseRedirect(reverse('account:profile',args=(id,)))

