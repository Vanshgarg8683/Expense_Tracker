from django.shortcuts import render, redirect
from django.contrib import messages
from tracker.models import transaction
from django.contrib.auth.models import User
from django.db.models import Sum
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.
def registration(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        
        userobj = User.objects.filter(username=username, email=email)
        if userobj.exists():
            messages.error(request, 'username or email already taken')
            return redirect('/registration')
        
        userobj =   User.objects.create(
            username = username, 
            email = email,
        )
        userobj.set_password(password)
        userobj.save()
        messages.success(request, 'Account has been created successfully')
        return redirect('/login')
    
    return render(request, 'registration.html')

def loginpage(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        userobj = User.objects.filter(username=username)
        if not userobj.exists():
            messages.error(request, 'Incorrect Username')
            return redirect('/login')
        
        userobj = authenticate(username = username, password=password)
        if not userobj:
            messages.error(request, 'Incorrect Credentials!')

        login(request, userobj)
        messages.success(request, 'You have logged in successfully!')
        return redirect('/')
    
    return render(request, 'login.html')
def logoutpage(request):
    logout(request)
    messages.success(request, 'logged out successfully!')
    return redirect('/login')
@login_required(login_url = '/login')
def index(request):
    if(request.method=="POST"):
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        transaction.objects.create(
            description=description,
            amount=amount,
            created_by=request.user
        )
    context = {
        'transaction' : transaction.objects.filter(created_by=request.user), 
        'balance' : transaction.objects.all().aggregate(balance = Sum('amount'))['balance'] or 0.00,
        'income' : transaction.objects.filter(created_by=request.user, amount__gte = 0).aggregate(income = Sum('amount'))['income'] or 0.00,
        'expense' : transaction.objects.filter(created_by=request.user, amount__lte = 0).aggregate(expense = Sum('amount'))['expense'] or 0.00
    }
    return render(request, 'index.html', context)


def remove(request, uuid):
    transaction.objects.get(uuid = uuid, created_by=request.user).delete()
    return redirect('/')