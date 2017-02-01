from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from .models import Users, Pokes
from django.contrib import messages
from django.contrib.auth import logout
from django.db.models import F, Count, Sum
from django import db
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


def index(request):
    return render(request, 'poke/index.html')

def register(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        conf_password = request.POST['conf_password']
        name = request.POST['name']
        alias = request.POST['alias']
        bday = request.POST['bday']
        errors = Users.objects.validation(email, password, conf_password, name, alias, bday)
        if type(errors) == list:
            for error in errors:
                messages.error(request, error);
            return redirect('/')
        else:
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            user = Users.objects.create(email=email, pw_hash=pw_hash, name=name, alias=alias)
            messages.success(request, "You have registered successfully! Please login")
            user.save()
            return redirect('/')

def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        result = Users.objects.login(email, password)
        if type(result) == list:
            for info in result:
                messages.info(request, info);
            return redirect('/')
        else:
            request.session['logged_user'] = result.id
            return redirect('/pokes')

def log_out(request):
    if request.method == "POST":
        currentUser = Users.objects.get(id = request.session['logged_user'])
        logout(request)
        return redirect('/')

def dash(request):
    currentUser = Users.objects.get(id=request.session['logged_user'])
    current_users = Users.objects.exclude(id=currentUser.id)
    pokes = Pokes.objects.filter(user=currentUser).values('poked_by__name').annotate(count=Count(F('poked_by_id'))).order_by("-count")
    pokers = Pokes.objects.filter(user=currentUser).values('poked_by__name').annotate(n_count=Sum('poked_by_id'))
    n = pokers.count()
    context ={
        'currentUser':currentUser,
        'current_users':current_users,
        'pokes':pokes,
        'n':n
    }
    return render(request, 'poke/dash.html', context)

def create_poke(request, id):
    if request.method == "POST":
        Pokes.objects.create(user = Users.objects.get(id=id), poked_by = Users.objects.get(id=request.session['logged_user']))
        poked_user = Users.objects.get(id=id)
        total = poked_user.total_pokes
        Users.objects.filter(id=id).update(total_pokes = total + 1)
        return redirect('/pokes')
